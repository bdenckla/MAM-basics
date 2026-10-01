import py_html.legacy_html as aht_html

import yeivin_itm.substitutions as sub

import yeivin_itm.content.my_yeivin_sec_345 as s345
import yeivin_itm.content.my_yeivin_sec_346 as s346
import yeivin_itm.content.my_yeivin_sec_347 as s347
import yeivin_itm.content.my_yeivin_sec_348 as s348
import yeivin_itm.content.my_yeivin_sec_349 as s349
import yeivin_itm.content.my_yeivin_sec_350 as s350
import yeivin_itm.content.my_yeivin_sec_351 as s351
import yeivin_itm.content.my_yeivin_sec_352 as s352
import yeivin_itm.content.my_yeivin_sec_353 as s353
import yeivin_itm.content.my_yeivin_sec_354 as s354
import yeivin_itm.content.my_yeivin_sec_355 as s355
import yeivin_itm.content.my_yeivin_sec_356 as s356
import yeivin_itm.content.my_yeivin_sec_357 as s357


def _cmn(as_str):
    return aht_html.maybe_join(as_str, ["Phonetic ", sub.cgaya])


TOCSEC = {
    "tocsec-part": sub.PART_3_NAME,
    "tocsec-include-in-top-page": True,
    "tocsec-title": _cmn(as_str=True),
    "tocsec-heading": _cmn(as_str=False),
    "tocsec-numsecs-before-titsecs": {345: s345.SEC},
    "tocsec-titsecs": [
        {
            "titsec-heading": [
                sub.cgaya(),
                " Marking a ",
                sub.cshewa(),
                " that Follows as Vocal",
            ],
            "titsec-numsecs": {346: s346.SEC},
        },
        {
            "titsec-heading": [sub.cgaya(), " on a Short Vowel"],
            "titsec-numsecs": {
                347: s347.SEC,
                348: s348.SEC,
                349: s349.SEC,
                350: s350.SEC,
            },
        },
        {
            "titsec-heading": [
                sub.cgaya(),
                " before the First of an Identical Pair of Letters",
            ],
            "titsec-numsecs": {351: s351.SEC},
        },
        {
            "titsec-heading": [sub.cgaya(), " on a Long Vowel"],
            "titsec-numsecs": {352: s352.SEC, 353: s353.SEC},
        },
        {
            "titsec-heading": [sub.cgaya(), " on a Short Vowel before a Guttural"],
            "titsec-numsecs": {354: s354.SEC, 355: s355.SEC},
        },
        {
            "titsec-heading": ["The System of Preference for Phonetic ", sub.cgaya()],
            "titsec-numsecs": {356: s356.SEC},
        },
        {
            "titsec-heading": [
                sub.maqqef(cap=True),
                " after ",
                sub.cgaya(),
                " after a Conjunctive",
            ],
            "titsec-numsecs": {357: s357.SEC},
        },
    ],
}
