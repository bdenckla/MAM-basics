from mb_cmn import file_io
from mb_cmn import hebrew_verse_numerals as hvn
from ac_wiki.book_names import LATIN_TO_HEBREW
from mb_cmn.my_utils import sum_of_map


def write_wikitext_file(grouped, out_path):
    lines = sum_of_map(_lines_for_one_book, grouped.items())
    file_io.with_tmp_openw(out_path, {}, _write_callback, lines)


def _lines_for_one_book(bkna_and_entries):
    lat_bkna, entries = bkna_and_entries
    heb_bkna = LATIN_TO_HEBREW[lat_bkna]
    line_1_for_book = "=== " + heb_bkna + " ==="
    line_2_for_book = "'''" + heb_bkna + " ...'''"
    lines_for_entries = sum_of_map(_lines_for_one_entry, entries)
    return ["", line_1_for_book, line_2_for_book, *lines_for_entries]


def _lines_for_one_entry(entry):
    url = entry["de_url"]
    leaf = entry["de_leaf"]
    if not url:
        return [f"# {leaf} N/A"]
    visible = _heb_range(entry["de_text_range"])
    anchor = f"[{url} {visible}]"
    daf_num_ab = _rv_ab(leaf)
    daf = f"(דף {daf_num_ab})"
    main_line = "#" + anchor + " " + daf
    gap = entry["de_gap"]
    if not gap:
        return [main_line]
    if gap == "Before":
        return ["# gap", main_line]
    if gap == "After":
        return [main_line, "# gap"]
    assert False, gap


def _heb_range(text_range):
    start_bcv, stop_bcv = text_range
    sta = _heb_bcv(start_bcv)
    sto = _heb_bcv(stop_bcv)
    sta_str = f"{sta[0]} {sta[1]},{sta[2]}"
    abbr_stop_str = _abbreviated_stop(sta, sto)
    return f"{sta_str}{_EN_DASH}{abbr_stop_str}"


def _abbreviated_stop(sta, sto):
    if sta[0] == sto[0]:
        if sta[1] == sto[1]:
            return sto[2]
        return f"{sto[1]},{sto[2]}"
    return f"{sto[0]} {sto[1]},{sto[2]}"


def _heb_bcv(bcv):
    lat_bkna, int_chnu, int_vrnu = bcv
    heb_bkna = LATIN_TO_HEBREW[lat_bkna]
    heb_chnu = hvn.INT_TO_STR_DIC[int_chnu]
    heb_vrnu = hvn.INT_TO_STR_DIC[int_vrnu]
    return heb_bkna, heb_chnu, heb_vrnu


def _rv_ab(leaf):  # r becomes א; v becomes ב
    return leaf[:-1] + _RV_AB[leaf[-1]]


def _write_callback(lines, out_fp):
    for line in lines:
        out_fp.write(line + "\n")


_EN_DASH = "–"
_RV_AB = {
    "r": "א",
    "v": "ב",
}
