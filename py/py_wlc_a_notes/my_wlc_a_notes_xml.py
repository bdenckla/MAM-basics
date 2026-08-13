"""Exports write_xml."""

import xml.etree.ElementTree as ET
import mb_cmn.file_io as file_io

# import py_uxlc.my_uxlc as my_uxlc
# import py_uxlc.my_uxlc_book_abbreviations as u_bk_abbr
import py_uxlc.my_uxlc_unicode_names as my_uxlc_unicode_names
import py_wlc.my_wlc_bcv_str as my_wlc_bcv_str
import py_wlc_a_notes.my_wlc_a_notes_native as native
import py_wlc_a_notes.my_wlc_a_notes_etan as etan
import py_wlc_a_notes.my_wlc_a_notes_utils as my_wlc_a_notes_utils
import py_wlc_a_notes.my_wlc_a_notes as my_wlc_a_notes
from mb_cmn import paths


def write(io_records):
    """Write records out in UXLC change proposal format."""
    dated_change_set = ET.Element("date")
    ET.SubElement(dated_change_set, "date").text = "2024.02.09"
    posrecdic = _posrecdic()
    uxlc = {}
    for io_record in io_records:
        ucp_seq = io_record.get("uxlc-change-proposal-sequential")
        if ucp_seq is not None:
            io_record["pos-within-verse"] = _pos_within_verse(io_record, posrecdic)
            change_elem = etan.top_elem(dated_change_set, "change")
            _add_misc(uxlc, change_elem, io_record)
            io_record["path-to-ucp"] = native.write_to_html(
                change_elem["native"], io_record
            )
    dated_change_set_tree = ET.ElementTree(dated_change_set)
    #
    ET.indent(dated_change_set_tree)
    #
    path = "all_uxlc_change_proposals.xml"
    file_io.with_tmp_openw(
        str(paths.wlc_pages_dir() / "wlc-a-notes" / path),
        {},
        _etree_write_callback,
        dated_change_set_tree,
    )
    return path


def _posrecdic():
    return {posrec["wlc-index"]: posrec for posrec in my_wlc_a_notes.POSITION_RECORDS}


def _pos_within_verse(record, posrecdic):
    wlc_index = record["wlc-index"]
    posrec = posrecdic[wlc_index]
    return posrec["pos-within-verse"]


def _etree_write_callback(xml_elementtree, out_fp):
    xml_elementtree.write(out_fp, encoding="unicode")
    out_fp.write("\n")


def _add_misc(io_uxlc, change_elem, record):
    _add_n(change_elem, record)
    _add_citation(io_uxlc, change_elem, record)
    _add_author(change_elem)
    _add_description(change_elem, record)
    _add_lc(change_elem, record)
    _add_xtext_xuni(change_elem, record, "reftext", "refuni")
    _add_xtext_xuni(change_elem, record, "changetext", "changeuni")
    _add_notes(change_elem, record)
    _add_analysistags(change_elem, record)
    _add_transnotes(change_elem, record)
    _add_status(change_elem)
    _add_type(change_elem)


def _add_n(change_elem, record):
    ucp_seq = record["uxlc-change-proposal-sequential"]
    etan.sub_elem_text(change_elem, "n", str(ucp_seq))


def _add_citation(io_uxlc, change_elem, record):
    citation_elem = etan.sub_elem(change_elem, "citation")
    #
    wlc_bcv_str = record["bcv"]
    uxlc_bkid = my_wlc_bcv_str.get_uxlc_bkid(wlc_bcv_str)
    chnu, vrnu = my_wlc_bcv_str.get_cv_pair(wlc_bcv_str)
    bcv = uxlc_bkid, chnu, vrnu
    word_position = _word_position(io_uxlc, record, bcv)
    #
    etan.sub_elem_text(citation_elem, "book", uxlc_bkid)
    etan.sub_elem_text(citation_elem, "c", str(chnu))
    etan.sub_elem_text(citation_elem, "v", str(vrnu))
    etan.sub_elem_text(citation_elem, "position", str(word_position))


def _word_position(io_uxlc, record, bcv):
    if position := record.get("pos-within-verse"):
        return position
    assert False
    # qere_atom = _qere_atom(record)
    # position = _word_position2(io_uxlc, qere_atom, bcv)
    # print_out = {
    #     'wlc-index': record['wlc-index'],
    #     'qere_atom': qere_atom,
    #     'pos-within-verse': position
    # }
    # print(print_out)
    # return position


# def _word_position2(io_uxlc, qere_atom, bcv):
#     verse_words = _get_verse_words(io_uxlc, bcv)
#     index = verse_words.index(qere_atom)
#     assert index != -1
#     return index + 1


# def _get_verse_words(io_uxlc, bcv):
#     uxlc_bkid, chnu, vrnu = bcv
#     if uxlc_bkid not in io_uxlc:
#         std_bkid = u_bk_abbr.BKNA_MAP_UXLC_TO_STD[uxlc_bkid]
#         io_uxlc[uxlc_bkid] = my_uxlc.read(std_bkid)
#     chidx = chnu - 1
#     vridx = vrnu - 1
#     return io_uxlc[uxlc_bkid][chidx][vridx]


def _add_author(change_elem):
    author_elem = etan.sub_elem(change_elem, "author")
    etan.sub_elem_text(author_elem, "name", "Ben Denckla")
    etan.sub_elem_text(author_elem, "mail", "bdenckla@alum.mit.edu")
    etan.sub_elem_text(author_elem, "confirmed", "true")


def _add_description(change_elem, record):
    atiss_eng = record["at issue English"]
    desc = f"Note that while creating the pointed qere, the transcriber {atiss_eng}"
    etan.sub_elem_text(change_elem, "description", desc)


def _line_excluding_blanks(record):
    if "line-excluding-blanks" in record:
        return record["line-excluding-blanks"]
    return record["line"]


def _add_lc(change_elem, record):
    lc_elem = etan.sub_elem(change_elem, "lc")
    etan.sub_elem_text(lc_elem, "folio", str(record["folio"]))
    etan.sub_elem_text(lc_elem, "column", str(record["column"]))
    etan.sub_elem_text(lc_elem, "line", str(_line_excluding_blanks(record)))
    etan.sub_elem_text(lc_elem, "credit", "Credit: Sefaria.org.")


def _add_xtext_xuni(change_elem, record, xtext, xuni):
    qere_atom = _qere_atom(record)
    xuni_str = my_uxlc_unicode_names.names(qere_atom)
    etan.sub_elem_text(change_elem, xtext, qere_atom)
    etan.sub_elem_text(change_elem, xuni, xuni_str)


def _add_notes(change_elem, record):
    notes_elem = etan.sub_elem(change_elem, "notes")
    if "qere-atom-at-issue" in record:
        fqere = record["qere"]  # full qere
        fqere_note = f"The qere atom at issue is part of the qere compound {fqere}."
        etan.sub_elem_text(notes_elem, "note", fqere_note)
    if "qere-context" in record:
        fqere = record["qere-context"]  # full qere
        fqere_note = (
            f"The qere at issue is part of the compound {fqere}. "
            "The other parts of this compound are not part of this qere."
        )
        etan.sub_elem_text(notes_elem, "note", fqere_note)
    mpk_note = _mpk_note_aued_for_dc(record["MPK"])
    etan.sub_elem_text(notes_elem, "note", mpk_note)
    for remark in record["remarks"]:
        etan.sub_elem_text(notes_elem, "note", _aued_for_dc(remark))
    side_notes = record.get("side-notes") or []
    for side_note in side_notes:
        snt, sns = my_wlc_a_notes_utils.side_note_string(side_note)
        if snt == "sn-blockquote":  # snt: side-note type
            sns = f"«{sns}»"
        sns = sns.replace("@", "").replace("#", "")
        sns = _aued_for_dc(sns)
        etan.sub_elem_text(notes_elem, "note", sns)


_AUED = "א\N{HEBREW MARK UPPER DOT}"
_AUED_WITH_EXP = f"{_AUED} (א with an extraordinary upper dot)"


def _mpk_note_aued_for_dc(mpk):
    # use aued (alef with an extraordinary upper dot) instead of dc (dotted circle)
    mpk_aued = mpk.replace("\N{DOTTED CIRCLE}", _AUED)
    if _AUED in mpk_aued:
        exp = f" (We use {_AUED_WITH_EXP} to hold marks not associated with a parent letter.)"
    else:
        exp = ""
    return f"The manuscript’s pointed ketiv (MPK) is {mpk_aued}.{exp}"


def _aued_for_dc(string):
    return string.replace("dotted circle", _AUED_WITH_EXP)


def _add_analysistags(change_elem, record):
    if dotan := record.get("Dotan"):
        assert dotan == "UXLC disagrees with BHL Appendix A"
    #
    # For all the words in the 39 records, UXLC agrees with BHL (body).
    # Four of the 39 have entries in BHL Appendix A.
    # UXLC disagrees with all four of them.
    # Sadly, the "analysistags" element of a UXLC change proposal
    # does not allow us to distinguish these two cases.
    # So in all cases we just say "aBHL", meaning "UXLC agrees with BHL (body)".
    #
    atags_elem = etan.sub_elem(change_elem, "analysistags")
    etan.sub_elem(atags_elem, "aBHL")


def _add_transnotes(change_elem, record):
    trnotes_elem = etan.sub_elem(change_elem, "transnotes")
    trnote_elem = etan.sub_elem(trnotes_elem, "transnote")
    etan.sub_elem_text(trnote_elem, "action", "Add")
    etan.sub_elem_text(trnote_elem, "type", "a")
    btxt = _beforetext(record)
    etan.sub_elem_text(trnote_elem, "beforetext", btxt)


def _beforetext(record):
    atiss = record["at issue"]
    qere_atom = _qere_atom(record)
    index = qere_atom.find(atiss)
    assert index != -1
    index2 = index + len(atiss)
    while index2 < len(qere_atom) and qere_atom[index2] not in _LETTERS:
        index2 += 1
    return record["qere"][:index2]


def _add_status(change_elem):
    etan.sub_elem_text(change_elem, "status", "Pending")


def _add_type(change_elem):
    etan.sub_elem_text(change_elem, "type", "NoTextChange")


def _qere_atom(record):
    return record.get("qere-atom-at-issue") or record["qere"]


_LETTERS = "אבגדהוזחטיךכלמםןנסעףפץצקרשת"

# <n>1</n>
# <citation>
#     <book>Dan</book>
#     <c>2</c>
#     <v>16</v>
#     <position>8</position>
# </citation>
# <author>
#     <name>Daniel Holman</name>
#     <mail>daniel.holman@mail.com</mail>
#     <confirmed>true</confirmed>
# </author>
# <description>Note possible dagesh in the first nun and weak dot in tsere under the tav.  Add note 't'.</description>
# <lc>
#     <folio>Folio_438B</folio>
#     <column>2</column>
#     <line>24</line>
#     <credit>Credit: Sefaria.org.</credit>
# </lc>
# <reftext>יִנְתֵּן־</reftext>
# <refuni>yod     hiriq     nun     sheva     tav     dagesh     tsere     final-nun     maqaf     </refuni>
# <changetext>יִנְתֵּן־</changetext>
# <changeuni>yod     hiriq     nun     sheva     tav     dagesh     tsere     final-nun     maqaf     </changeuni>
# <notes>
#     <note>The text is in good condition near this word. A reddish blob appears in nun; it is poorly formed and ill-positioned, compared to the dagesh in the tav. The blob will not be transcribed as a dagesh. The leading dot in the tsere under the tav is reddish and small but well-formed and well positioned. It will remain a tsere.</note>
#     <note>BHL has no dagesh in the nun and a tsere under the tav.  BHLA has no entry for this verse.</note>
# </notes>
# <analysistags>
#     <aBHL/>
# </analysistags>
# <transnotes>
#     <transnote>
#         <action>Add</action>
#         <type>t</type>
#         <beforetext>יִנְ</beforetext>
#     </transnote>
# </transnotes>
# <status>Pending</status>
# <type>NoTextChange</type>
