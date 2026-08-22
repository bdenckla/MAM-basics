from mb_cmn import file_io
from mb_cmn import hebrew_verse_numerals as hvn
from lenin_wiki import image_urls as iu
from mb_cmn import bib_locales as tbn
from py_misc import get_cvm_rec_from_bcvt as gcrfb
from py_misc import vtrad_helpers as helpers
from lenin_wiki import masorah_finalis_lines as mfl
from mb_cmn.mam_bknas_and_std_bknas import he_bk39_name
from mb_cmn.my_utils import sum_of_map, sl_map


def write_wikitext_file(grouped, out_path):
    main_lines = sum_of_map(_lines_for_one_book, grouped.items())
    mafi_lines = mfl.masorah_finalis_lines()
    lines = main_lines + mafi_lines
    file_io.with_tmp_openw(out_path, {}, _write_callback, lines)


def _lines_for_one_book(bkna_and_rows):
    bk39id_mostly, rows = bkna_and_rows
    if bk39id_mostly in (_MAS_LISTS_TORAH, _MAS_LISTS_PROPHETS):
        heb_bkna = bk39id_mostly
        lines_for_rows = sl_map((_line_for_any_row, bk39id_mostly), rows)
    else:
        heb_bkna = he_bk39_name(bk39id_mostly)
        lines_for_rows = sl_map(_line_for_bib_row, rows)
    line_1_for_book = "=== " + heb_bkna + " ==="
    line_2_for_book = "'''" + heb_bkna + " ...'''"
    return ["", line_1_for_book, line_2_for_book, *lines_for_rows]


def _line_for_bib_row(row):
    visible = _heb_range(_text_range(row))
    return _line_for_any_row(visible, row)


def _line_for_any_row(visible, row):
    page_ddda = row["page"]
    assert page_ddda
    urls = iu.image_urls(page_ddda)
    anchor_lcci = f"[{urls['lcci']} <nowiki>{visible}</nowiki>]"
    anchor_sefa = f"[{urls['sefa']} ספריא]"
    # We use <nowiki>...</nowiki> to avoid problems when there are square brackets in "visible".
    daf_num_ab = iu.cacb_hahb(page_ddda)
    daf = f"(דף {daf_num_ab})"
    return f"# {anchor_lcci} / {anchor_sefa} {daf}"


def _text_range(row):
    sta_bcvy = _mref(row, "startrec", "chnu", "vrnu", "wordnu", "max_wordnu")
    sto_bcvy = _mref(row, "stoprec", "chnu", "vrnu", "wordnu", "max_wordnu")
    return sta_bcvy, sto_bcvy


def _mref(row, stxkey, keyc, keyv, keyp, keyl):
    stxrec = row[stxkey]
    maxp = stxrec[keyl]  # max value of p is the length of the verse
    assert maxp != 1
    if stxrec[keyp] == 1:
        fml = "fml-first"
    elif stxrec[keyp] == maxp:
        fml = "fml-last"
    else:
        fml = "fml-mid"
    return row["bkid"], stxrec[keyc], stxrec[keyv], fml


def _heb_range(text_range):
    sta_bcvy, sto_bcvy = text_range
    sta = _get_heb_bcv_imt_fr_bcv_ibt(sta_bcvy[:3])
    sto = _get_heb_bcv_imt_fr_bcv_ibt(sto_bcvy[:3])
    sta_str = f"{sta[0]} {sta[1]},{sta[2]}"
    abbr_sto_str = _abbreviated_sto(sta, sto)
    pasus = _pasu(text_range)
    return f"{sta_str}{pasus[0]}{_EN_DASH}{abbr_sto_str}{pasus[1]}"


def _pasu(text_range):
    # pasu: partial suffix: 2 for mid-verse start, 1 for mid-verse stop
    sta_bcvy, sto_bcvy = text_range
    sta_fml, sto_fml = sta_bcvy[3], sto_bcvy[3]
    sta_pasu = "" if sta_fml == "fml-first" else "2"
    sto_pasu = "" if sto_fml == "fml-last" else "1"
    return sta_pasu, sto_pasu


def _abbreviated_sto(sta, sto):
    if sta[0] == sto[0]:
        if sta[1] == sto[1]:
            return sto[2]
        return f"{sto[1]},{sto[2]}"
    return f"{sto[0]} {sto[1]},{sto[2]}"


def _get_heb_bcv_imt_fr_bcv_ibt(bcv_ibt):
    """
    Get a Hebrew bcv IMT from a [Latin/int] bcv IBT.
    IMT: in the MAM vtrad
    IBT: in the BHS vtrad
    """
    bcvtbhs = tbn.mk_bcvtbhs(*bcv_ibt)
    cvm_rec = gcrfb.get_cvm_rec_from_bcvt(bcvtbhs)
    if cvm_rec is None:
        return _get_heb_bcv(bcv_ibt)
    cvve_type, cvm = gcrfb.cvm_rec_get_parts(cvm_rec)
    assert cvve_type in _PARTIAL_AND_SAME
    # Partial is okay because partial means that
    # this is a BHS verse that corresponds to only part of a MAM verse.
    # I.e. the MAM verse number is "less precise"
    # than the BHS verse number we're coming from.
    return _get_heb_bcv((bcv_ibt[0], cvm[0], cvm[1]))


_PARTIAL_AND_SAME = helpers.CVVE_TYPE_SAME_CONTENTS, helpers.CVVE_TYPE_PARTIAL_CONTENTS


def _get_heb_bcv(bcv):
    bk39id, int_chnu, int_vrnu = bcv
    heb_bkna = he_bk39_name(bk39id)
    heb_chnu = hvn.INT_TO_STR_DIC[int_chnu]
    heb_vrnu = hvn.INT_TO_STR_DIC[int_vrnu]
    return heb_bkna, heb_chnu, heb_vrnu


def _write_callback(lines, out_fp):
    for line in lines:
        out_fp.write(line + "\n")


_EN_DASH = "–"
_MAS_LISTS_TORAH = "Masoretic lists: Number of verses and the sections in the Torah"
_MAS_LISTS_PROPHETS = (
    "Masoretic lists: Number of verses and the sections in the Prophets"
)
