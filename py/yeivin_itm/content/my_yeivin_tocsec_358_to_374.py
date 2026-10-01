import yeivin_itm.substitutions as sub
import yeivin_itm.content.my_yeivin_amisc_sec_not_yet_transcribed as sec_not_yet_transcribed

_CMN = "The Accents in the Three Books"
TOCSEC = {
    "tocsec-part": sub.PART_3_NAME,
    "tocsec-title": _CMN,
    "tocsec-heading": _CMN,
    "tocsec-numsecs-before-titsecs": {},
    "tocsec-titsecs": [
        {
            "titsec-heading": sub.revia_gadol(cap=True),
            "titsec-numsecs": {363: sec_not_yet_transcribed.SEC},
        },
        {
            "titsec-heading": sub.tsinnor(cap=True),
            "titsec-numsecs": {365: sec_not_yet_transcribed.SEC},
        },
        {
            "titsec-heading": sub.revia_qatan(cap=True),
            "titsec-numsecs": {368: sec_not_yet_transcribed.SEC},
        },
        {
            "titsec-heading": sub.legarmeh(cap=True),
            "titsec-numsecs": {370: sec_not_yet_transcribed.SEC},
        },
    ],
}
