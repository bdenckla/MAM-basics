import py_html.legacy_html as aht_html

import yeivin_itm.substitutions as sub

import yeivin_itm.content.my_yeivin_sec_318 as s318
import yeivin_itm.content.my_yeivin_sec_319 as s319
import yeivin_itm.content.my_yeivin_sec_320 as s320
import yeivin_itm.content.my_yeivin_sec_321 as s321
import yeivin_itm.content.my_yeivin_sec_322 as s322
import yeivin_itm.content.my_yeivin_sec_323 as s323
import yeivin_itm.content.my_yeivin_sec_324 as s324
import yeivin_itm.content.my_yeivin_sec_325 as s325
import yeivin_itm.content.my_yeivin_sec_326 as s326
import yeivin_itm.content.my_yeivin_sec_327 as s327
import yeivin_itm.content.my_yeivin_sec_328 as s328
import yeivin_itm.content.my_yeivin_sec_329 as s329
import yeivin_itm.content.my_yeivin_sec_330 as s330
import yeivin_itm.content.my_yeivin_sec_331 as s331
import yeivin_itm.content.my_yeivin_sec_332 as s332
import yeivin_itm.content.my_yeivin_sec_333 as s333
import yeivin_itm.content.my_yeivin_sec_334 as s334
import yeivin_itm.content.my_yeivin_sec_335 as s335
import yeivin_itm.content.my_yeivin_sec_336 as s336
import yeivin_itm.content.my_yeivin_sec_337 as s337
import yeivin_itm.content.my_yeivin_sec_338 as s338
import yeivin_itm.content.my_yeivin_sec_339 as s339
import yeivin_itm.content.my_yeivin_sec_340 as s340
import yeivin_itm.content.my_yeivin_sec_341 as s341
import yeivin_itm.content.my_yeivin_sec_342 as s342
import yeivin_itm.content.my_yeivin_sec_343 as s343
import yeivin_itm.content.my_yeivin_sec_344 as s344


def _cmn(as_str):
    return aht_html.maybe_join(as_str, ["Musical ", sub.cgaya])


TOCSEC = {
    "tocsec-part": sub.PART_3_NAME,
    "tocsec-include-in-top-page": True,
    "tocsec-title": _cmn(as_str=True),
    "tocsec-heading": _cmn(as_str=False),
    "tocsec-numsecs-before-titsecs": {318: s318.SEC},
    "tocsec-titsecs": [
        {
            "titsec-heading": sub.TITSEC_HEADING_319,
            "titsec-numsecs": {319: s319.SEC},
        },
        {
            "titsec-heading": ["“Fully Regular” Structure"],
            "titsec-numsecs": {320: s320.SEC, 321: s321.SEC},
        },
        {
            "titsec-heading": ["“Almost Fully Regular” Structure"],
            "titsec-numsecs": {322: s322.SEC, 323: s323.SEC},
        },
        {
            "titsec-heading": ["Non-regular Structure"],
            "titsec-numsecs": {324: s324.SEC},
        },
        {
            "titsec-heading": [sub.cgaya(), " before ", sub.paseq(cap=True)],
            "titsec-numsecs": {325: s325.SEC},
        },
        {
            "titsec-heading": [*sub.gaya_osr(cap=True)],
            "titsec-numsecs": {
                326: s326.SEC,
                327: s327.SEC,
                328: s328.SEC,
                329: s329.SEC,
                330: s330.SEC,
                331: s331.SEC,
            },
        },
        {
            "titsec-heading": [sub.cgaya(), " on an Open, Post-stress Syllable"],
            "titsec-numsecs": {332: s332.SEC},
        },
        {
            "titsec-heading": [sub.cgaya(), " with ", sub.cshewa()],
            "titsec-numsecs": {
                333: s333.SEC,
                334: s334.SEC,
                335: s335.SEC,
                336: s336.SEC,
            },
        },
        {
            "titsec-heading": [sub.cgaya(), " on a ", sub.mclv(cap=True), " Syllable"],
            "titsec-numsecs": {337: s337.SEC},
        },
        {
            "titsec-heading": [
                sub.cgaya(),
                " on a Closed, ",
                sub.tsere(cap=True),
                "-vowelled, Post-stress Syllable",
            ],
            "titsec-numsecs": {338: s338.SEC},
        },
        {
            "titsec-heading": ["The System of Preference for Musical ", sub.cgaya()],
            "titsec-numsecs": {339: s339.SEC, 340: s340.SEC, 341: s341.SEC},
        },
        {
            "titsec-heading": [
                "The Marking of ",
                sub.cgaya(),
                " in Manuscripts and Printed Texts",
            ],
            "titsec-numsecs": {342: s342.SEC, 343: s343.SEC, 344: s344.SEC},
        },
    ],
}
