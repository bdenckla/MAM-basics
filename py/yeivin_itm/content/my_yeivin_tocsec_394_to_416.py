import py_html.legacy_html as aht_html

import yeivin_itm.substitutions as sub
import yeivin_itm.helpers as hlp

import yeivin_itm.content.my_yeivin_sec_394 as s394
import yeivin_itm.content.my_yeivin_sec_395 as s395
import yeivin_itm.content.my_yeivin_sec_396 as s396
import yeivin_itm.content.my_yeivin_sec_397 as s397
import yeivin_itm.content.my_yeivin_sec_398 as s398
import yeivin_itm.content.my_yeivin_sec_399 as s399
import yeivin_itm.content.my_yeivin_sec_400 as s400
import yeivin_itm.content.my_yeivin_sec_401 as s401
import yeivin_itm.content.my_yeivin_sec_402 as s402
import yeivin_itm.content.my_yeivin_sec_403 as s403
import yeivin_itm.content.my_yeivin_sec_404 as s404
import yeivin_itm.content.my_yeivin_sec_405 as s405
import yeivin_itm.content.my_yeivin_sec_406 as s406
import yeivin_itm.content.my_yeivin_sec_407 as s407
import yeivin_itm.content.my_yeivin_sec_408 as s408
import yeivin_itm.content.my_yeivin_sec_409 as s409
import yeivin_itm.content.my_yeivin_sec_410 as s410
import yeivin_itm.content.my_yeivin_sec_411 as s411
import yeivin_itm.content.my_yeivin_sec_412 as s412
import yeivin_itm.content.my_yeivin_sec_413 as s413
import yeivin_itm.content.my_yeivin_sec_414 as s414
import yeivin_itm.content.my_yeivin_sec_415 as s415
import yeivin_itm.content.my_yeivin_sec_416 as s416

TITSEC_1 = {
    "titsec-heading": [sub.mappiq(cap=True), " and ", sub.shureq(cap=True), " Dot"],
    "titsec-numsecs": {
        394: s394.SEC,
        395: s395.SEC,
        396: s396.SEC,
    },
}
TITSEC_2 = {
    "titsec-heading": ["The Marking of ", sub.rafe(cap=True)],
    "titsec-numsecs": {
        397: s397.SEC,
        398: s398.SEC,
    },
}
TITSEC_3 = {
    "titsec-heading": [
        sub.begad_kefat(cap=True),
        " after ",
        sub.comma_list_of_heb_ahw_or_y(),
    ],
    "titsec-numsecs": {
        399: s399.SEC,
        400: s400.SEC,
        401: s401.SEC,
        402: s402.SEC,
    },
}
TITSEC_4 = {
    "titsec-heading": [
        sub.dexiq(cap=True),
        " ",
        hlp.paren(["Conjunctive ", sub.dagesh(cap=True)]),
    ],
    "titsec-numsecs": {
        403: s403.SEC,
        404: s404.SEC,
        405: s405.SEC,
        406: s406.SEC,
    },
}
TITSEC_5 = {
    "titsec-heading": [sub.dexiq(cap=True), " in other situations"],
    "titsec-numsecs": {
        407: s407.SEC,
        408: s408.SEC,
    },
}
TITSEC_6 = {
    "titsec-heading": [sub.dagesh(cap=True), " after מַה and זֶה"],
    "titsec-numsecs": {
        409: s409.SEC,
        410: s410.SEC,
    },
}
TITSEC_7 = {
    "titsec-heading": [sub.dagesh(cap=True), " used to Divide or Distinguish"],
    "titsec-numsecs": {
        411: s411.SEC,
        412: s412.SEC,
        413: s413.SEC,
        414: s414.SEC,
    },
}
TITSEC_8 = {
    "titsec-heading": [
        "The Function and Value of Special uses of ",
        sub.dagesh(cap=True),
    ],
    "titsec-numsecs": {
        415: s415.SEC,
        416: s416.SEC,
    },
}


def _cap_dagesh(as_str):
    return sub.dagesh(cap=True, as_str=as_str)


def _cap_rafe(as_str):
    return sub.rafe(cap=True, as_str=as_str)


def _cmn(as_str):
    return aht_html.maybe_join(as_str, [_cap_dagesh, " and ", _cap_rafe])


TOCSEC = {
    "tocsec-part": sub.PART_4_NAME,
    "tocsec-include-in-top-page": True,
    "tocsec-title": _cmn(as_str=True),
    "tocsec-heading": _cmn(as_str=False),
    "tocsec-numsecs-before-titsecs": {},
    "tocsec-titsecs": [
        TITSEC_1,
        TITSEC_2,
        TITSEC_3,
        TITSEC_4,
        TITSEC_5,
        TITSEC_6,
        TITSEC_7,
        TITSEC_8,
    ],
}
