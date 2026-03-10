_AMMP = "(AMMP is the accent/maqaf/meteg profile.)"
_TSIT_POST = "that after tsinnorit, the AMMP is"
_TSIT_PRE = "that before tsinnorit, the AMMP is"
EXPLANATIONS = {
    ("(mah)",): f"{_TSIT_POST} mahapakh. {_AMMP}",
    ("(mah),(rev)",): f"{_TSIT_POST} mahapakh and revia. {_AMMP}",
    ("(mah),(mos)",): f"{_TSIT_POST} mahapakh and mtgoslq. {_AMMP}",
    ("(mer)",): f"{_TSIT_POST} merkha. {_AMMP}",
    ("-(mah)",): f"{_TSIT_POST} maqaf and mahapakh. {_AMMP}",
    ("-(mer)",): f"{_TSIT_POST} maqaf and merkha. {_AMMP}",
    (
        "-(mer),(mos)-(mos)",
    ): f"{_TSIT_POST} maqaf, merkha, mtgoslq, maqaf, and mtgoslq. {_AMMP}",
    #
    ("pre", "-"): f"{_TSIT_PRE} maqaf. {_AMMP}",
    ("pre", "(mos)"): f"{_TSIT_PRE} mtgoslq. {_AMMP}",
    ("pre", "(mos)-"): f"{_TSIT_PRE} mtgoslq, maqaf. {_AMMP}",
    ("pre", "(mer)-"): f"{_TSIT_PRE} merkha, maqaf. {_AMMP}",
}
