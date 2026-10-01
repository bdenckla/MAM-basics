import yeivin_itm.substitutions as sub

import yeivin_itm.content.my_yeivin_sec_375 as s375

_CMN = "Introduction"
TOCSEC = {
    "tocsec-part": sub.PART_4_NAME,
    "tocsec-include-in-top-page": True,
    "tocsec-title": _CMN,
    "tocsec-heading": _CMN,
    "tocsec-numsecs-before-titsecs": {375: s375.SEC},
    "tocsec-titsecs": [],
}
