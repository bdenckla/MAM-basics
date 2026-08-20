from mb_cmn.shrink import shrink
from boj_render import boj_html


def enrich_one_qr_by_flattening_strs(quirkrec):
    """Flatten nested HTML content in comment fields to shrunk flat lists.

    Args:
        quirkrec: partially-enriched quirkrec dict. The fields
            qr-what-is-weird, qr-generic-comment, and qr-bhq-comment
            are flattened if present.
    """
    wiw = quirkrec["qr-what-is-weird"]
    gencom = quirkrec.get("qr-generic-comment")
    bhqcom = quirkrec.get("qr-bhq-comment")
    flat_wiw = _flatten_yyycom(wiw)
    flat_gencom = gencom and _flatten_yyycom(gencom)
    flat_bhqcom = bhqcom and _flatten_yyycom(bhqcom)
    new_wiw = {"qr-what-is-weird": flat_wiw} if flat_wiw else {}
    new_gencom = {"qr-generic-comment": flat_gencom} if flat_gencom else {}
    new_bhqcom = {"qr-bhq-comment": flat_bhqcom} if flat_bhqcom else {}
    return {**quirkrec, **new_wiw, **new_gencom, **new_bhqcom}


def _flatten_yyycom(yyycom):
    if isinstance(yyycom, str):
        return yyycom
    assert isinstance(yyycom, list)
    flat = boj_html.flatten(yyycom)
    return shrink(flat)
