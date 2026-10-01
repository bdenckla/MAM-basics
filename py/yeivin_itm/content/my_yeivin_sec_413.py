import yeivin_itm.helpers as hlp
import yeivin_itm.substitutions as sub

_FTNT = sub.footnote(
    ["Meaning, “can be ", hlp.emphasis("accidentally"), " assimilated”?"]
)
SEC = [
    sub.para(
        [
            ["In cases where the same letter ends one word and starts the next,"],
            [" $dagesh is not generally used in early Tiberian manuscripts."],
            [" However, the Masorah records that ben Naftali used $dagesh"],
            [" in the first ", sub.nun(), " of ", hlp.hbo("נוּן")],
            [" in the pair ", hlp.hbo("בִּן־נוּן"), sub.thspc()],
            [" i.e., ben Naftali’s pointing was ", hlp.hbo("בִּן־נּוּן")],
            [" while ben Asher did not use $dagesh in that ", sub.nun(), "."],
            [" In a few manuscripts, such as"],
            [" ", sub.ms_lenin(), ", $dagesh"],
            [" is sometimes used on the first letter of the second word"],
            [
                " in pairs like ",
                hlp.hboloc("וַיִּתֶּן־לּ֖וֹ", "@Gen 24:36"),
            ],  # MAM וַיִּתֶּן־ל֖וֹ
            [sub.thspc(), " where the first word ends with "],
            [sub.nun(), ", and the second word begins with ", sub.lamed(), "."],
            [
                " So also ",
                hlp.hboloc("וַיִּתֶּן־לּ֤וֹ", "@1K 11:19"),
            ],  # MAM וַיִּתֶּן־ל֤וֹ
            [" in the JTS manuscript 226."],
            [
                " On ",
                hlp.hboloc("וְיִתֶּן־לִ֗י אֶת־מְעָרַ֤ת הַמַּכְפֵּלָה֙", "@Gen 23:9"),
            ],
            [sub.thspc(), " Redaq (רד״ק) (Qimḥi) noted (Miklol 72b)"],
            [" “The ", sub.nun(), " can be ", hlp.ftntjoin("assimilated", _FTNT)],
            [" to the ", sub.lamed(), " of ", hlp.hbo("לִי"), sub.thspp(), "”"],
            [" It appears, then that this $dagesh"],
            [" also serves to emphasize the division between the two words"],
            [" to avoid the assimilation of the ", sub.nun(), "."],
        ]
    )
]
