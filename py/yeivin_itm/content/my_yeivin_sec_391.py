import yeivin_itm.substitutions as sub

SEC = [
    sub.para(
        [
            "In some manuscripts, such as ",
            sub.ms_aleppo(),
            ", $x_shewa is often used"
            " on non-guttural letters in all the categories described."
            " In others, like ",
            sub.ms_s_507(),
            ", this is rare. Clearly the Masoretes considered the use of a"
            " $x_shewa sign to mark $vocshewa",
            " on a guttural as necessary, but on other letters as optional."
            " Thus, for instance, the ",
            sub.diqduqe_dotan_sec_num(19),
            " says:",
        ]
    ),
    sub.blockquote_p(
        [
            "Some scribes, following a valid tradition, read ",
            sub.x_qamets(),
            " in many places ..."
            " while others, also following a valid tradition, do not,"
            " but there is no (authoritative) source but the preference of the scribes.",
        ]
    ),
    sub.para(["Similarly the ", sub.horayat_d(64, 372), " says:"]),
    sub.blockquote_p(
        [
            "If one argues that the ",
            sub.dalet(),
            " of “Mordecai” (and other letters in other words) has ",
            sub.x_qamets(),
            ", tell him,"
            " “but this sign is only a device used by some scribes"
            " to warn that the letters should be pronounced fully,"
            " and not slurred over.” ",
            sub.x_qamets(mwcap="mwcap-type-sentence-case"),
            ""
            " is written in some texts."
            " It is not used in others, but the"
            " reader nevertheless pronounces the word in the same way when he"
            " comes to read it.",
        ]
    ),
]
