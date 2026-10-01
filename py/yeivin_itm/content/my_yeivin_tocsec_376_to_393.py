import yeivin_itm.substitutions as sub

import yeivin_itm.content.my_yeivin_sec_376 as s376
import yeivin_itm.content.my_yeivin_sec_377 as s377
import yeivin_itm.content.my_yeivin_sec_378 as s378
import yeivin_itm.content.my_yeivin_sec_379 as s379
import yeivin_itm.content.my_yeivin_sec_380 as s380
import yeivin_itm.content.my_yeivin_sec_381 as s381
import yeivin_itm.content.my_yeivin_sec_382 as s382
import yeivin_itm.content.my_yeivin_sec_383 as s383
import yeivin_itm.content.my_yeivin_sec_384 as s384
import yeivin_itm.content.my_yeivin_sec_385 as s385
import yeivin_itm.content.my_yeivin_sec_386 as s386
import yeivin_itm.content.my_yeivin_sec_387 as s387
import yeivin_itm.content.my_yeivin_sec_388 as s388
import yeivin_itm.content.my_yeivin_sec_389 as s389
import yeivin_itm.content.my_yeivin_sec_390 as s390
import yeivin_itm.content.my_yeivin_sec_391 as s391
import yeivin_itm.content.my_yeivin_sec_392 as s392
import yeivin_itm.content.my_yeivin_sec_393 as s393

_THE_RECOGNITION_OF_VOCAL_SHEWA_I_THE_GENERAL_RULE = [
    "The Recognition of Vocal ",
    sub.cshewa(),
    " (i): The General Rule",
]
_THE_RECOGNITION_OF_VOCAL_SHEWA_II_SPECIAL_CASES = [
    "The Recognition of Vocal ",
    sub.cshewa(),
    " (ii): Special Cases",
]
_THE_PRONUNCIATION_OF_SHEWA = ["The Pronunciation of ", sub.cshewa()]
_SHEWA_ON_A_NON_GUTTURAL_LETTER = [sub.x_shewa(cap=True), " on a Non-Guttural Letter"]
_PREFIXES_WITH_SHEWA_BEFORE_YOD_WITH_XIREQ = [
    "Prefixes with ",
    sub.cshewa(),
    " before ",
    sub.yod(cap=True),
    " with ",
    sub.xireq(cap=True),
]
TOCSEC = {
    "tocsec-part": sub.PART_4_NAME,
    "tocsec-include-in-top-page": True,
    "tocsec-title": sub.cshewa(as_str=True),
    "tocsec-heading": sub.cshewa(),
    "tocsec-numsecs-before-titsecs": {
        376: s376.SEC,
    },
    "tocsec-titsecs": [
        {
            "titsec-heading": _THE_RECOGNITION_OF_VOCAL_SHEWA_I_THE_GENERAL_RULE,
            "titsec-numsecs": {
                377: s377.SEC,
                378: s378.SEC,
                379: s379.SEC,
                380: s380.SEC,
            },
        },
        {
            "titsec-heading": _THE_RECOGNITION_OF_VOCAL_SHEWA_II_SPECIAL_CASES,
            "titsec-numsecs": {
                381: s381.SEC,
                382: s382.SEC,
                383: s383.SEC,
                384: s384.SEC,
                385: s385.SEC,
                386: s386.SEC,
            },
        },
        {
            "titsec-heading": _THE_PRONUNCIATION_OF_SHEWA,
            "titsec-numsecs": {387: s387.SEC},
        },
        {
            "titsec-heading": _SHEWA_ON_A_NON_GUTTURAL_LETTER,
            "titsec-numsecs": {
                388: s388.SEC,
                389: s389.SEC,
                390: s390.SEC,
                391: s391.SEC,
            },
        },
        {
            "titsec-heading": _PREFIXES_WITH_SHEWA_BEFORE_YOD_WITH_XIREQ,
            "titsec-numsecs": {
                392: s392.SEC,
                393: s393.SEC,
            },
        },
    ],
}
