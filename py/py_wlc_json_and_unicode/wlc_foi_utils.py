"""Exports write."""

import mb_cmn.file_io as file_io
import py_wlc_json_and_unicode.wlc_utils as wlc_utils
import py_wlc_json_and_unicode.wlc_uword as wlc_uword
import py_wlc_json_and_unicode.wlc_release_info as ri
import py_wlc_json_and_unicode.wlc_foi_utils_uni as fuu


def write(out_path, wlc_id, parsed):
    io_fois = _init()
    _flexcollect(io_fois, wlc_id, parsed, _collect)
    if ri.encoding_is_uni(wlc_id):
        io_fois["fragile_foi"] = fuu.ff_init()
        _flexcollect(io_fois, wlc_id, parsed, fuu.collect_uni)
    #
    io_fois["notes_foi"] = _sort_notes_foi(io_fois["notes_foi"])
    #
    file_io.json_dump_to_file_path(io_fois, f"{out_path}/2fois.json")


def kqwrite(out_path, wlc_id, kqparsed):
    io_fois = _kqinit()
    _flexcollect(io_fois, wlc_id, kqparsed, _kqcollect)
    file_io.json_dump_to_file_path(io_fois, f"{out_path}/2fois.json")


def _flexcollect(io_fois, wlc_id, xparsed, xcollect):
    for verse in xparsed["verses"]:
        bcv = verse["bcv"]
        for velsod in verse["vels"]:
            xcollect(io_fois, wlc_id, bcv, velsod)


def _init():
    return {
        "sam_pe_inun_foi": {"P": 0, "S": 0, "N": 0},
        "notes_foi": {"nf-counts": {}, "nf-cases": []},
    }


def _kqinit():
    return {
        "kq_foi": {
            "kq-counts": {
                "k1q1": 0,
                "k0q1": 0,
                "k1q0": 0,
                "k2q1": 0,
                "k1q2": 0,
                "k2q2": 0,
            },
            "kq-cases": [],
        }
    }


def _sort_notes_foi(notes_foi):
    nfc = notes_foi["nf-counts"]
    nfc_sorted = dict(sorted(nfc.items()))
    notes_foi_out = {
        "nf-counts": nfc_sorted,
        "nf-cases": notes_foi["nf-cases"],
    }
    return notes_foi_out


def _collect(io_fois, wlc_id, bcv, velsod):
    if spi := wlc_utils.get_sam_pe_inun(velsod):
        sam_pe_inun_foi = io_fois["sam_pe_inun_foi"]
        sam_pe_inun_foi[spi] += 1
        return
    if notes := wlc_utils.get_notes(velsod):
        word = velsod["word"]
        counts, cases = _deref2(io_fois["notes_foi"], "nf-counts", "nf-cases")
        for note in notes:
            if note not in counts:
                counts[note] = 0
            counts[note] += 1
            cases.append(_make_case(wlc_id, bcv, notes, note, word))


def _make_case(wlc_id, bcv, notes, note, word):
    notes_str = "".join(notes)
    case = {}
    case["note"] = note
    case["bcv"] = bcv
    if ri.encoding_is_mdc(wlc_id):
        case["uword"] = wlc_uword.uword(word)
    case["word"] = word
    case["notes_str"] = notes_str
    return case


def _kqcollect(io_fois, wlc_id, bcv, velsod):
    if ketiv_and_qere := wlc_utils.get_kq(velsod):
        ketiv_and_qere = velsod["kq"]
        lenk = len(ketiv_and_qere[0])
        lenq = len(ketiv_and_qere[1])
        knqm = f"k{lenk}q{lenq}"
        #
        counts, cases = _deref2(io_fois["kq_foi"], "kq-counts", "kq-cases")
        #
        counts[knqm] += 1
        if knqm != "k1q1":
            case = {"knqm": knqm, "bcv": bcv, **_k2q2_generic(ketiv_and_qere)}
            cases.append(case)


def _k2q2_generic(ketiv_and_qere):
    out = {"k1": None, "k2": None, "q1": None, "q2": None}
    kkeys = {0: "k1", 1: "k2"}
    for kidx, kvelsod in enumerate(ketiv_and_qere[0]):
        out[kkeys[kidx]] = _word(kvelsod)
    qkeys = {0: "q1", 1: "q2"}
    for qidx, qvelsod in enumerate(ketiv_and_qere[1]):
        out[qkeys[qidx]] = _word(qvelsod)
    return out


def _word(velsod):
    if isinstance(velsod, str):
        return velsod
    return velsod.get("word")


def _deref2(foi, counts_key, cases_key):
    return foi[counts_key], foi[cases_key]
