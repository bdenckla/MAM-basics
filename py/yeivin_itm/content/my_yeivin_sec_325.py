import yeivin_itm.substitutions as sub
import yeivin_itm.helpers as hlp

_FSTK_2_30_PHRASE = sub.join_with_paseq(str("וַיֹּ֥אמֶֽר"), str("לֹ֖א"))
_FTNT = sub.footnote(sub.explain_paseq())
_FTNT_2 = sub.footnote(
    [
        "Other cases like that include ",
        hlp.hboloc(sub.join_with_paseq("וַיֹּ֣אמֶֽר", "לֹ֔א"), "@1K 11:22"),
        " and ",
        hlp.hboloc(sub.join_with_paseq("וַיֹּ֥אמֶֽר", "לֹֽא׃"), "@Jud 12:5"),
        sub.thspp(),
    ]
)
_CONT_PARA = [
    ["This is most commonly found in cases like "],
    [hlp.lhbo("@1K 2:30", _FSTK_2_30_PHRASE), hlp.ftntjoin(sub.thspc(), _FTNT)],
    [" where it is evidently used to mark a separation "],
    ["between the two words greater than that indicated by the "],
    [sub.paseq(), hlp.ftntjoin(".", _FTNT_2)],
    [" $Gaya is only marked in this position in early manuscripts,"],
    [" and is rare even there."],
]

SEC = [sub.para(_CONT_PARA)]
