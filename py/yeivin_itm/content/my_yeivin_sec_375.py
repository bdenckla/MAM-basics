import yeivin_itm.helpers as hlp
import yeivin_itm.substitutions as sub

SEC = [
    sub.para(
        [
            "Masoretic treatises such as the following"
            " naturally deal with matters of vocalization:"
        ]
    ),
    sub.unordered_list(
        [
            ["the ", hlp.rom("Kitāb al-Khilaf"), " (", sub.sefer_ha_xillufim(), ")"],
            ["the ", sub.diqduqe()],
            ["the “Treatise on the $Shewa”"],
            ["the ", sub.horayat()],
        ]
    ),
    sub.para(
        [
            "These are outside the scope of this book, but two phenomena,",
            " $dagesh and $shewa,",
            " form such an important part of the subject matter of such treatises"
            " that it seems advisable to include a discussion of them in an appendix."
            " It must be noted, however, that they are discussed here from"
            " the point of view of the masoretic treatises, which is"
            " different from that of modern grammarians."
            " So, statements made here may conflict with modern grammars"
            " (particularly introductory grammars),"
            " since statements made here are based on historical considerations.",
        ]
    ),
]
