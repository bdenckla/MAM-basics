from urllib.parse import quote

import py_html.wlc_utils_html as wlc_utils_html
import py_uxlc.my_uxlc_book_abbreviations as u_bk_abbr
import mb_cmn.bib_locales as tbn
from mb_cmn.uxlc_change_url import uxlc_change_url
from mb_cmn import paths
from mb_cmn import site_links

# The folder of the pages whose MAM-with-doc links this module builds, the full records
# of the WLC 4.20-to-4.22 changes: a link to another page of the site is relative to it
# (mb_cmn/site_links.py).
_FULL_RECORD_FOLDER = site_links.folder_below_root(
    paths.wlc_pages_dir() / "420422" / "full-record"
)


def bcv_with_link_to_tdu(record):
    uxlc_bcv_str = _uxlc_bcv_str(record)
    href = _tanach_dot_us_url(record)
    return wlc_utils_html.anchor(uxlc_bcv_str, {"href": href})


def bcv_with_link_to_mwd(record):
    uxlc_bcv_str = _uxlc_bcv_str(record)
    href = _mam_with_doc_url(record)
    return wlc_utils_html.anchor(uxlc_bcv_str, {"href": href})


def uxlc_change_with_link(release_and_id):
    _release_date, change_id = release_and_id
    return wlc_utils_html.anchor(
        change_id, {"href": _url_for_uxlc_change(release_and_id)}
    )


def _uxlc_bcv_str(record):
    std_bcv_triple = record["std-bcv-triple"]
    std_bkid = std_bcv_triple[0]
    uxlc_bkid = u_bk_abbr.BKNA_MAP_STD_TO_UXLC[std_bkid]
    chnu, vrnu = std_bcv_triple[1], std_bcv_triple[2]
    return f"{uxlc_bkid}{chnu}:{vrnu}"


def _tanach_dot_us_url(record):
    uxlc_bcv_str = _uxlc_bcv_str(record)
    return f"https://tanach.us/Tanach.xml?{uxlc_bcv_str}"


def _mam_with_doc_url(record):
    std_bcv_triple = record["std-bcv-triple"]
    std_bkid = std_bcv_triple[0]
    osdf = tbn.ordered_short_dash_full_39(std_bkid)  # e.g. A2-Exodus
    chnu, vrnu = std_bcv_triple[1], std_bcv_triple[2]
    # Above, we're ignoring verse numbering differences
    # quote matters for exactly one osdf: "E1-Song of Songs" has a space in it.
    page = quote(f"{osdf}.html")
    bcv_part = f"{page}#c{chnu}v{vrnu}"
    return site_links.site_href_from_folder(
        _FULL_RECORD_FOLDER, f"MAM-with-doc/{bcv_part}"
    )


def _url_for_uxlc_change(release_and_id):
    release_date, change_id = release_and_id
    return uxlc_change_url(release_date, change_id)
