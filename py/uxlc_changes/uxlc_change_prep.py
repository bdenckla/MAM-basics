"""Exports date_qualify_and_reformat"""

import re

import uxlc_misc.my_uxlc_book_abbreviations as u_bk_abbr
import uxlc_changes.uxlc_authors as uxlc_authors
import uxlc_changes.uxlc_unicode_names as uxlc_unicode_names


def date_qualify_and_reformat(date, change):
    """
    Qualify the change given with the date given.
    Also reformat various fields of the change given.
    """
    change["n"] = int(change["n"])
    #
    if notes := change.get("notes"):
        change["notes"] = _listify(notes["note"])
    else:
        change["notes"] = []
    assert _is_list_of_str(change["notes"])
    #
    change["authors"] = _listify(change["author"])
    del change["author"]
    change["authors"] = list(map(_collapse_author, change["authors"]))
    #
    change["citation"] = _collapse_citation(change["citation"])
    lc_loc, lc_loc_gen = _collapse_lc(change["lc"])
    change["lc"] = lc_loc
    change["lc_gen"] = lc_loc_gen  # generated lc (if != orig lc)
    #
    an_tags = change.get("analysistags") or {}
    if "analysistags" in change:
        del change["analysistags"]
    change = {**change, **_simplify_analysis_tags(an_tags)}
    change["transnotes"] = None
    #
    change["refuni_gen"] = _uni_matches_text(change, "ref")
    change["changeuni_gen"] = _uni_matches_text(change, "change")
    change["changeuni_erbs"] = _changeuni_eq_refuni_but_shouldnt(change)
    #
    return {"changeset": date, **change}


def _listify(list_or_nonlist):
    if isinstance(list_or_nonlist, list):
        return list_or_nonlist
    return [list_or_nonlist]


def _collapse_author(author):
    assert tuple(author.keys()) == ("name", "mail", "confirmed")
    name = author["name"]
    mail = author["mail"]
    confirmed = author["confirmed"]
    mac = mail, confirmed
    macn = uxlc_authors.MAIL_AND_CONFIRMED[name]
    assert mac == macn or mac in macn
    return name


def _collapse_citation(citation):
    keys = "book", "c", "v", "position"
    assert tuple(citation.keys()) == keys
    book_name = citation["book"]
    assert book_name in u_bk_abbr.BKNA_MAP_UXLC_TO_STD, book_name
    book_name_normalized = _normalize_book_name(book_name)
    int_keys = "c", "v", "position"
    chnu, vrnu, wpos = tuple(int(citation[k]) for k in int_keys)
    return f"{book_name_normalized} {chnu}:{vrnu}.{wpos}"


def _normalize_book_name(book_name_uxlc):
    book_name_std = u_bk_abbr.BKNA_MAP_UXLC_TO_STD[book_name_uxlc]
    return u_bk_abbr.BKNA_MAP_STD_TO_UXLC[book_name_std]


ALT_CREDITS = [
    " ".join(
        (
            "Credit: Photograph by Bruce and Kenneth Zuckerman, West Semitic",
            "Research, in collaboration with Ancient Biblical Manuscript",
            "Center. Courtesy National Library of Russia",
            "(Saltykov-Shchedrin).",
        )
    ),
    ".",  # (just period!) in '2020.09.29'-1
    "Photo by author, cropped by publisher.",
    "Credit: Internet Archive (archive.org)",
    "Credit: Internet Archive (archive.org).",
]


def _credit_is_okay(credit):
    if credit is None:  # credit is None happens in 2020.01.30-1
        return True
    if credit in ALT_CREDITS:
        return True
    #
    # Some standard (Sefaria) credit fields lack period after 'Credit: Sefaria.org'.
    #
    # Below, we use "startswith" rather than == (equals) because in at least
    # one case, the "credit" field is also used to make a comment about the
    # image, in relation to the change proposal.
    #
    # For example, the "credit" field of 2022.12.10-31 says
    # (after saying "Credit: Sefaria.org."):
    #
    #     The complete LC line 18, words 9-12, are shown.
    #
    return credit.startswith("Credit: Sefaria.org")


def _collapse_lc(lc_location):
    keys = "folio", "column", "line", "credit"
    assert tuple(lc_location.keys()) == keys
    folio, folio_gen = _parse_folio(lc_location["folio"])
    credit = lc_location["credit"]
    assert _credit_is_okay(credit)
    line = lc_location["line"]
    column = lc_location["column"]
    if lc_location["line"] != "1-2":
        assert re.fullmatch(r"\d+", line)
    assert re.fullmatch(r"\d+", column)
    lc_gen = f"{folio_gen} {column}:{line}" if folio_gen else None
    return f"{folio} {column}:{line}", lc_gen


def _parse_folio(folio):
    exceptions = {
        "Folio_142A (NOT Folio_141B)": "Folio_142A",
        "Folio_190AB": "Folio_190A",
    }
    folio_norm1 = exceptions.get(folio) or folio
    folio_patt = r"Folio_(F?)(0?\d\d?\d?)([AaBRrv])"
    match = re.fullmatch(folio_patt, folio_norm1)
    assert match, folio_norm1
    gr_digits = match.group(2)
    gr_recto_verso = match.group(3)
    leaf_int = int(gr_digits)
    rv_remaps = {"A": "A", "B": "B", "a": "A", "R": "A", "r": "A", "v": "B"}
    ca_or_cb = rv_remaps[gr_recto_verso]  # capital A or capital B
    folio_gen = f"Folio_{leaf_int:03d}{ca_or_cb}"
    if folio != folio_gen:
        return folio, folio_gen
    return folio, None


def _uni_matches_text(change, ref_or_change):
    """Make sure that, for example, the following two things correspond:

        The code points in change['reftext']
        The code point names in change['refuni']

    E.g. makes sure that a reftext of "לֵ֣ךְ" corresponds to a refuni of
    "lamed tsere munah final-kaf sheva".  # translit-ok: UXLC's own refuni vocabulary

    Note that:

        The keys ending in "uni" (refuni & changeuni) are the keys for the
        strings containing Unicode code point names.

        The keys ending in "text" (reftext & changetext) are the keys for the
        Unicode strings themselves, i.e. the strings of Unicode code points.
    """
    keys = {
        "ref": ("reftext", "refuni"),
        "change": ("changetext", "changeuni"),
    }
    cp_key, cpname_key = keys[ref_or_change]
    cp_str = change[cp_key]  # e.g. change['reftext']
    cpnames_str = change[cpname_key]  # e.g. change['refuni']
    if cp_str is None and cpnames_str is None:
        return None
    cp_str_ne = cp_str.replace("!", "")  # ne: no exclamation [mark]
    # Exclamation mark appears in str (but not in names) where
    # there is a pre-existing transcription note
    cpnames_new = list(map(uxlc_unicode_names.name, cp_str_ne))
    cpnames_str = cpnames_str.replace("etnachta", "etnahta")  # translit-ok: UXLC name
    cpnames_str = cpnames_str.replace("gereshayim", "gershayim")
    cpnames_str = cpnames_str.replace("cgj", "combining-grapheme-joiner")
    cpnames = cpnames_str.split(" ")
    return " ".join(cpnames_new) if cpnames_new != cpnames else None


def _changeuni_eq_refuni_but_shouldnt(change):
    cu_eq_ru = change["changeuni"] == change["refuni"]
    ct_eq_rt = change["changetext"] == change["reftext"]
    return cu_eq_ru and not ct_eq_rt


def _is_list_of_str(obj):
    if not isinstance(obj, list):
        return False
    return all(isinstance(s, str) for s in obj)


def _simplify_analysis_tags(an_tags):
    columns = {"aBHL": None, "aBHLA": None, "D2T": None, "T2D": None}
    for tag in an_tags:
        assert tag in columns
        columns[tag] = True
    return columns
