_TSIT_POST = "that after tsinnorit, the AMMP is"
_TSIT_PRE = "that before tsinnorit, the AMMP is"
EXPLANATIONS = {
    ("(mah)",): f"{_TSIT_POST} mahapakh",
    ("(mah),(rev)",): f"{_TSIT_POST} mahapakh and revia",
    ("(mah),(mos)",): f"{_TSIT_POST} mahapakh and mtgoslq",
    ("(mer)",): f"{_TSIT_POST} merkha",
    ("-(mah)",): f"{_TSIT_POST} maqaf and mahapakh",
    ("-(mer)",): f"{_TSIT_POST} maqaf and merkha",
    ("-(mer),(mos)-(mos)",): (
        f"{_TSIT_POST} maqaf, merkha, mtgoslq, maqaf, and mtgoslq"
    ),
    #
    ("pre", "-"): f"{_TSIT_PRE} maqaf",
    ("pre", "(mos)"): f"{_TSIT_PRE} mtgoslq",
    ("pre", "(mos)-"): f"{_TSIT_PRE} mtgoslq, maqaf",
    ("pre", "(mer)-"): f"{_TSIT_PRE} merkha, maqaf",
}


OVERALL_EXPLANATION = (
    " ".join(
        (
            "This page groups cases involving tsinnorit by the nearby AMMP, i.e.",
            "the accent/maqaf/meteg profile associated with the relevant context.",
        )
    ),
    " ".join(
        (
            "Labels without a pre prefix describe the AMMP after tsinnorit; labels",
            "with pre describe the AMMP before tsinnorit.",
        )
    ),
)
