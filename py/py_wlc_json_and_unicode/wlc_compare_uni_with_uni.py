import mb_cmn.file_io as file_io
import py_wlc_json_and_unicode.wlc_utils as wlc_utils
import py_wlc_json_and_unicode.wlc_compare_vyls_uni as cvu


def compare(wlca, wlcb, out_path_fn):
    """Compare wlca with wlcb (e.g. WLC 4.20 with WLC 4.22)"""
    # Ignore headers in the comparison.
    io_diff = {
        "ids": [wlca["id"], wlcb["id"]],
        "type changes": [],
        "notes differences": [],
        "word differences": [],
    }
    verse_list_a, verse_list_b = wlca["verses"], wlcb["verses"]
    assert len(verse_list_a) == len(verse_list_b)
    for verse_ab in zip(verse_list_a, verse_list_b):
        verse_a, verse_b = verse_ab
        assert verse_a["bcv"] == verse_b["bcv"]
        _compare_verse(io_diff, verse_a["bcv"], verse_a["vels"], verse_b["vels"])
    file_io.json_dump_to_file_path(io_diff, out_path_fn(io_diff["ids"]))


def _compare_verse_element(io_diff, bcv, vela, velb):
    vyla = wlc_utils.velsod_to_veldic(vela)
    vylb = wlc_utils.velsod_to_veldic(velb)
    return cvu.compare_vyls(io_diff, bcv, vyla, vylb)


def _compare_verse(io_diff, bcv, velsa, velsb):
    assert len(velsa) == len(velsb)
    for vel_ab in zip(velsa, velsb):
        _compare_verse_element(io_diff, bcv, *vel_ab)
