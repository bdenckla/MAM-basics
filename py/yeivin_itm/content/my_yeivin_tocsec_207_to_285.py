import yeivin_itm.substitutions as sub
import yeivin_itm.content.my_yeivin_amisc_sec_not_yet_transcribed as sec_not_yet_transcribed
import yeivin_itm.content.my_yeivin_sec_239 as s239
import yeivin_itm.content.my_yeivin_sec_282 as s282

TITSEC_239 = {
    # In ITM, single quotes surround the word "Pashṭa" in the heading below.
    # This is because ITM uses italic styling for these headings
    # so it has to set off romanized words in a different way than the usual italic styling.
    # Instead of italic styling, it uses single quotes.
    "titsec-heading": ["The Repetition of the ", sub.pashta(cap=True), " Sign"],
    "titsec-numsecs": {
        239: s239.SEC,
    },
}

_CMN = "The Disjunctive Accents"
TOCSEC = {
    "tocsec-part": sub.PART_3_NAME,
    "tocsec-include-in-top-page": True,
    "tocsec-title": _CMN,
    "tocsec-heading": [f"{_CMN}: The Combinations Possible and their Servi"],
    "tocsec-numsecs-before-titsecs": {
        216: sec_not_yet_transcribed.SEC,
    },
    "tocsec-titsecs": [
        TITSEC_239,
    ],
    "tocsec-numsecs-after-titsecs": {
        248: sec_not_yet_transcribed.SEC,
        278: sec_not_yet_transcribed.SEC,
        282: s282.SEC,
        283: sec_not_yet_transcribed.SEC,
        284: sec_not_yet_transcribed.SEC,
    },
}
