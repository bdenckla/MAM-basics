"""Build entry dicts for explicit-xataf mappings."""

from pycmn import hebrew_points as hpo
from py_explicit_xataf.infer import _varika_positions


def make_entries(ref, varika_word, xataf_word, match_kind, sigla_detail):
    """Build entry dicts, splitting space-separated multi-word cases.

    E.g. Nehemiah 12:36 has "מִֽלְﬞלַ֡י גִּֽלְﬞלַ֡י" which becomes two entries.
    """
    vw_parts = varika_word.split(" ")
    xw_parts = xataf_word.split(" ")
    if len(vw_parts) > 1 and len(vw_parts) == len(xw_parts):
        return [
            _make_one_entry(ref, vw, xw, match_kind, sigla_detail)
            for vw, xw in zip(vw_parts, xw_parts)
            if hpo.VARIKA in vw
        ]
    return [_make_one_entry(ref, varika_word, xataf_word, match_kind, sigla_detail)]


def _make_one_entry(ref, varika_word, xataf_word, match_kind, sigla_detail):
    entry = {
        "ref": ref,
        "varika_word": varika_word,
        "xataf_word": xataf_word,
        "match_kind": match_kind,
    }
    if sigla_detail is not None:
        sigla = sigla_detail["sigla"]
        entry["sigla"] = sigla
        if "א" not in sigla and "ל" not in sigla:
            entry["neither-lc-nor-ac-mentioned"] = True
    vc = len(_varika_positions(varika_word))
    if vc > 1:
        entry["varika-count"] = vc
    return entry
