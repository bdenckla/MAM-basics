import mb_cmn.file_io as file_io
import py_wlc_json_and_unicode.wlc_utils as wlc_utils
import py_wlc_json_and_unicode.wlc_compare_vyls_mdc as cvm


def compare(wlca, wlcb, out_path_fn):
    """Compare wlca with wlcb (e.g. WLC 4.20 with WLC 4.22)"""
    # Ignore headers in the comparison.
    io_diff = {
        "ids": [wlca["id"], wlcb["id"]],
        "verses_of_different_length": [],
        "side_a_edits": [],
        "type changes": [],
        "notes differences": [],
        "word differences": [],
        "word positions of word differences": {},
    }
    verse_list_a, verse_list_b = wlca["verses"], wlcb["verses"]
    assert len(verse_list_a) == len(verse_list_b)
    for verse_ab in zip(verse_list_a, verse_list_b):
        verse_a, verse_b = verse_ab
        assert verse_a["bcv"] == verse_b["bcv"]
        _compare_verse(io_diff, verse_a["bcv"], verse_a["vels"], verse_b["vels"])
    file_io.json_dump_to_file_path(io_diff, out_path_fn(io_diff["ids"]))


def _compare_verse_element(io_diff, bcv, velidx, vela, velb):
    vyla = wlc_utils.velsod_to_veldic(vela)
    vylb = wlc_utils.velsod_to_veldic(velb)
    return cvm.compare_vyls(io_diff, bcv, velidx, vyla, vylb)


def _compare_verse(io_diff, bcv, velsa, velsb):
    velsa_comparable = _make_velsa_comparable(io_diff, bcv, velsa, velsb)
    assert len(velsa_comparable) == len(velsb)
    for velidx, vel_ab in enumerate(zip(velsa_comparable, velsb)):
        _compare_verse_element(io_diff, bcv, velidx, *vel_ab)


def _make_velsa_comparable(io_diff, bcv, velsa, velsb):
    if len(velsa) == len(velsb):
        return velsa
    diff_len_record = bcv, len(velsa), len(velsb)
    io_diff["verses_of_different_length"].append(diff_len_record)
    if bcv == "gn14:17":
        saer, velsa_c = _make_velsa_comparable_gn1417(velsa)
    elif bcv == "da2:39":
        saer, velsa_c = _make_velsa_comparable_da239(velsa)
    else:
        assert False, f"unexpected verse of differing length: {bcv}"
    io_diff["side_a_edits"].append({"bcv": bcv, **saer})
    return velsa_c


def _make_velsa_comparable_gn1417(velsa):
    part1part2 = _split_gn1417_word_9(velsa[8])
    side_a_edit_record = {
        "edit type": "split word",
        "original word": velsa[8],
        "split word": part1part2,
    }
    velsa_comparable = [*velsa[:8], *part1part2, *velsa[9:]]
    return side_a_edit_record, velsa_comparable


def _make_velsa_comparable_da239(velsa):
    side_a_edit_record = {
        "edit type": "added null word",
        "word before null word": velsa[3],
        "word after null word": velsa[4],
    }
    velsa_comparable = [*velsa[:4], None, *velsa[4:]]
    return side_a_edit_record, velsa_comparable


def _split_gn1417_word_9(word_9):
    assert word_9["word"] == "K.:DFRLF(O80MER"
    part1 = word_9["word"][:6]
    part2 = word_9["word"][6:]
    part1 = part1 + "→"
    part2 = "←" + part2
    return part1, {"word": part2, "notes": word_9["notes"]}
