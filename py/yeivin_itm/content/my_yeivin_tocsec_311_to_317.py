import py_html.legacy_html as aht_html

import yeivin_itm.substitutions as sub

import yeivin_itm.content.my_yeivin_sec_311 as s311
import yeivin_itm.content.my_yeivin_sec_312 as s312
import yeivin_itm.content.my_yeivin_sec_313 as s313
import yeivin_itm.content.my_yeivin_sec_314 as s314
import yeivin_itm.content.my_yeivin_sec_315 as s315
import yeivin_itm.content.my_yeivin_sec_316 as s316
import yeivin_itm.content.my_yeivin_sec_317 as s317


def _cmn(as_str):
    return aht_html.maybe_join(as_str, ["Initial Remarks on ", sub.cgaya])


TOCSEC = {
    "tocsec-part": sub.PART_3_NAME,
    "tocsec-include-in-top-page": True,
    "tocsec-title": _cmn(as_str=True),
    "tocsec-heading": _cmn(as_str=False),
    "tocsec-numsecs-before-titsecs": {},
    "tocsec-titsecs": [
        {"titsec-heading": ["Literature"], "titsec-numsecs": {311: s311.SEC}},
        {
            "titsec-heading": ["The Name ", sub.cgaya()],
            "titsec-numsecs": {312: s312.SEC},
        },
        {
            "titsec-heading": ["The ", sub.cgaya(), " Sign"],
            "titsec-numsecs": {313: s313.SEC, 314: s314.SEC},
        },
        {
            "titsec-heading": ["The Function of ", sub.cgaya()],
            "titsec-numsecs": {315: s315.SEC},
        },
        {
            "titsec-heading": ["The Categories of ", sub.cgaya()],
            "titsec-numsecs": {316: s316.SEC, 317: s317.SEC},
        },
    ],
}
