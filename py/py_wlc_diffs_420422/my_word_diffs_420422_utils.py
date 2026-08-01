import py_html.wlc_utils_html as wlc_utils_html
import mb_cmn.hebrew_accents as ha
import mb_cmn.hebrew_points as hpo
import mb_cmn.hebrew_punctuation as hpu


def uxlc_change_proposals(record):
    if ucp_or_ucps := record.get("UXLC-change-proposals"):
        if isinstance(ucp_or_ucps, list):
            ucps = ucp_or_ucps
        else:
            ucps = [ucp_or_ucps]
        return ucps
    return []


def diff_type_span_with_title(record):
    diff_type = record["diff-type"]
    return wlc_utils_html.span(diff_type, {"title": diff_type_long(record)})


def diff_type_long(record):
    diff_type = record["diff-type"]
    return _DIFF_TYPES[diff_type]


def diff_type_abbreviation_table():
    rows = list(map(_diff_type_abbreviation_row, _DIFF_TYPES.items()))
    toa_frag_id = "table-of-abbreviations"
    caption = wlc_utils_html.caption("Table of abbreviations")
    children = [caption, *rows]
    return toa_frag_id, wlc_utils_html.table(children, {"id": toa_frag_id})


def _diff_type_abbreviation_row(ad_pair):
    abbrev, definition = ad_pair
    datum_for_abbrev = wlc_utils_html.table_datum(abbrev)
    datum_for_defn = wlc_utils_html.table_datum(definition)
    return wlc_utils_html.table_row([datum_for_abbrev, datum_for_defn])


def _example(english, mark1, mark2):
    return f"{english}: א{mark1} to א{mark2}"


def _example_quad(english, mq1, mq2):
    x_to_y = (
        f"א{mq1[0]}א{mq1[1]}א{mq1[2]}א{mq1[3]} to א{mq2[0]}א{mq2[1]}א{mq2[2]}א{mq2[3]}"
    )
    return f"{english}: {x_to_y}"


MQ1 = hpo.SHEVA, hpo.XPATAX, hpo.XQAMATS, hpo.XSEGOL
MQ2 = "", hpo.PATAX, hpo.QAMATS, hpo.SEGOL_V
_DMS_EXAMPLE_1 = "וּלְרׇחְבָּ֑הּ"
_DMS_EXAMPLE_2 = "וּלְרׇחְבָּ֑הּ".replace(hpo.DAGOMOSD, "")
_DMS = "dagesh, mapiq, or shuruq dot"
_DIFF_TYPES = {
    "-dms": f"remove {_DMS}: {_DMS_EXAMPLE_1} to {_DMS_EXAMPLE_2}",
    "+dms": f"add {_DMS}: {_DMS_EXAMPLE_2} to {_DMS_EXAMPLE_1}",
    "-rfh": _example("remove rafeh", hpo.RAFE, ""),
    "-pashta": _example("remove pashta accent", ha.PASH, ""),
    "+rev": _example("add revia accent", "", ha.REV),
    "+psq": _example("add paseq", "", hpu.PASOLEG),
    "+mqf": _example("add maqaf", "", hpu.MAQ),
    "-shoḥ": _example_quad(
        "remove sheva or change ḥataf vowel to full vowel", MQ1, MQ2
    ),
    "+shoḥ": _example_quad("add sheva or change full vowel to ḥataf vowel", MQ2, MQ1),
    "vow-chng": "vowel change",
    "acc-chng": "accent change",
    "misc": "miscellaneous",
}
