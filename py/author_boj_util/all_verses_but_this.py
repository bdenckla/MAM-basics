from author_boj_util.english_list import english_list

# Job verses where L omits dagesh after מה
_NO_DAG_AFTER_MAH_VERSES = [
    "$link_16_6",
    "$link_21_15",
    "$link_34_33_VMH0YD3F",
    "$link_35_7",
]
_PTX_IS_NOT_XTF_VERSES = [
    "$link_9_35",
    "$link_27_9",
    "$link_34_33_HM3M5",
]
_LEG_MISSING_BEFORE_G3YH_RBY3_VERSES = [
    "$link_32_11",
    "$link_34_33_YJLMNH_2_of_2_FTW",
]


def ptx_is_not_xtf(cv: str) -> list[str]:
    return [
        "As $DM footnote 20 mentions, this is one of three such cases, the other two being",
        *[" ", _all_verses_but_this(_PTX_IS_NOT_XTF_VERSES, cv), "."],
        " In all three cases,",
        " the consensus has געיה on an initial vocal שווא notated as a חטף פתח.",
        " In μL, the געיה is on an initial פתח,",
        " a full (albeit short) syllable rather than a שווא.",
    ]


def no_dag_after_mah(cv: str) -> list[str]:
    return [
        "As $DM footnote 25 mentions, the omission of דגש after %מה־",
        *[" is common in μL. See ", _all_ndam_but_this(cv), "."],
    ]


def leg_missing_before_g3yh_rby3(cv: str) -> list[str]:
    others = _all_verses_but_this(_LEG_MISSING_BEFORE_G3YH_RBY3_VERSES, cv)
    return [
        "As $DM footnote 32 mentions, in two cases in Job,",
        " μL omits the לגרמיה stroke before a word with געיה and רביע.",
        *[" The other such case is ", others, "."],
        " In both cases, it looks like there may have been an erasure in between the words,",
        " where one would expect a לגרמיה to have been, if one was originally present in μL.",
    ]


_REITERATION_NEW_IN_BHQ_VERSES = [
    "$link_6_21",
    "$link_18_4_HLM3N5_2_of_2_FTW",
    "$link_19_16_QRAFY",
]


def reiteration_new_in_bhq(cv: str) -> str:
    others = _all_verses_but_this(_REITERATION_NEW_IN_BHQ_VERSES, cv)
    return (
        "This is one of the three reiterations that is new in $BHQ,"
        f" i.e. not present in $BHS. The other two are {others}."
    )


def _all_verses_but_this(verses: list[str], cv: str) -> str:
    """Return an English-formatted list of verses, excluding cv.

    Verses may be bare "C:V", or $-entries like "$link_C_V_WORDID"
    or "$plain_C_V".  The entry is retained as-is in the output so
    dollar_sub can resolve it.
    """
    others = [v for v in verses if _bare_cv(v) != cv]
    return english_list(others)


def _bare_cv(v: str) -> str:
    """Extract a plain chapter:verse from any verse representation.

    Handles: "C:V", "$link_C_V_WORDID", "$plain_C_V".
    """
    import re

    m = re.match(r"^\$(?:link|plain)_(\d+)_(\d+)", v)
    if m:
        return f"{int(m.group(1))}:{int(m.group(2))}"
    return v


def _all_ndam_but_this(cv: str) -> str:
    return _all_verses_but_this(_NO_DAG_AFTER_MAH_VERSES, cv)
