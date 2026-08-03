import uxlc_misc.my_uxlc_location as my_uxlc_location
import uxlc_misc.my_uxlc_book_abbreviations as u_bk_abbr


def extend_records(io_records):
    uxlc, pbi = my_uxlc_location.prep()
    for recidx, io_record in enumerate(io_records):
        io_record["original-order"] = recidx + 1
        io_record["std-bcv-triple"] = _std_bcv_triple(io_record)
        pg_and_gs = my_uxlc_location.page_and_guesses(
            uxlc, pbi, _std_bcvp_quad(io_record)
        )
        for key, val in pg_and_gs.items():
            io_record[key] = val


def _std_bcvp_quad(record):
    uxlc_bcvp = record["uxlc_bcvp"]
    uxlc_bkid = uxlc_bcvp[0]
    std_bkid = u_bk_abbr.BKNA_MAP_UXLC_TO_STD[uxlc_bkid]
    return std_bkid, uxlc_bcvp[1], uxlc_bcvp[2], uxlc_bcvp[3]


def _std_bcv_triple(record):
    return _std_bcvp_quad(record)[:-1]
