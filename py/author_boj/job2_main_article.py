"""Exports gen_html_file and anchor"""

from boj_render import boj_html
from author_boj.m_contributions_base import contributions_base
from author_boj.m_reiterations_base import reiterations_base
from author_boj.m_implications_base import implications_base
from author_boj.m_bad_news_1_base import bad_news_1_base
from author_boj_util.job2_bad_news_2 import (
    bad_news_2,
    wlc_dexi,
    wlc_dexi_group_info,
    wlc_misc,
    wlc_misc_group_info,
)
from author_boj_util.para_and_table import para_and_table
from author_boj_util.group_infos import (
    contributions_group_info,
    reiterations_group_info,
    implications_group_info,
    xbhq_and_n3_group_info,
)
from author_boj_util import author
from author_boj_util.all_quirks import AllQuirks
from author_boj_util.common_titles_etc import (
    D2_TITLE,
    D2_H1_CONTENTS,
    D2_FNAME,
    d3_anchor,
    d4_anchor,
)
from author_boj_util.num_range import num_range
from mb_cmn.my_utils import dv_map


def gen_html_file(aq: AllQuirks):
    author.assert_stem_eq(__file__, D2_FNAME)
    cbody = _make_cbody(aq)
    author.help_gen_html_file(aq.tdm_ch, D2_FNAME, D2_TITLE, cbody)


def _make_cbody(aq: AllQuirks):
    the_lens = dv_map(len, aq.qr_groups)
    len_wlc_dexi = the_lens["g:tbhq_and_zdw"]
    len_wlc_misc = the_lens["g:tbhq_and_zmw"]
    cbody = [
        author.heading_level_1(D2_H1_CONTENTS),
        author.para(_NOT_A_SCHOLARLY),
        author.para_ol(_CULT_OF_BHS, _BHS_FAILS),
        author.para(_BHQ_AS_BHS_ALTERNATIVE),
        author.para(_SOURED),
        author.para_ul(_BETTER_EDITIONS, _THE_THREE_EDITIONS),
        author.para(_MEGILLOTH_2004),
        author.para(_DM_PREDATES),
        author.para(_BHL_PREDATES),
        author.para(_AWARE_OF_BHL),
        author.para(_WE_ARE_NOW_LEFT),
        author.para(_JUDGES),
        author.para(_WLC_PREDATES),
        author.para_ul(_MY_PURPOSES, _CLIST_NOT_MY_CONCERN),
        author.para(_CPARA_NOT_MY_CONCERN),
        author.para(_SPECIFICS_OF_BHQ_JOB),
        para_and_table(
            aq, _contributions, contributions_group_info(the_lens["g:nbhq_and_x3"])
        ),
        author.para(_AFTER_CONTRIBUTIONS),
        para_and_table(
            aq, _reiterations, reiterations_group_info(the_lens["g:nbhq_and_n3"])
        ),
        para_and_table(
            aq, _implications, implications_group_info(the_lens["g:tbhq_and_n3"])
        ),
        para_and_table(
            aq, _bad_news_1, xbhq_and_n3_group_info(the_lens["g:xbhq_and_n3"])
        ),
        author.para(_after_bad_news_1_part_2(len(aq.qr_groups["g:nbhq_and_n3"]))),
        author.para(_AFTER_BAD_NEWS_1_PART_3),
        author.para(bad_news_2(len_wlc_dexi, len_wlc_misc)),
        para_and_table(aq, wlc_dexi, wlc_dexi_group_info(len_wlc_dexi)),
        para_and_table(aq, wlc_misc, wlc_misc_group_info(len_wlc_misc)),
        author.para_ul(_CONCLUSION, _conclusion_list(the_lens)),
        author.heading_level_2("Postscript 1: $UXLC"),
        author.para(_POSTSCRIPT_UXLC),
        author.heading_level_2("Postscript 2: quirks in μA"),
        author.para(_POSTSCRIPT_QUIRKS_IN_MU_A),
        author.heading_level_2("Related works by me"),
        author.para(_RELATED_WORKS_BY_ME),
    ]
    return cbody


_NOT_A_SCHOLARLY = [
    "It may come as a surprise to some that $BHQ Job",
    " does not include, at its core,",
    " a modern scholarly edition of the Masoretic Text.",
    #
    " $BHQ Job includes, at its core,",
    " a lightly updated version of what was, in 1977,",
    " a modern scholarly edition of the Masoretic Text: $BHS.",
    #
    " The claims I have just made about $BHQ Job",
    " are probably true of all fascicles of $BHQ released to date,",
    " judging from anecdotal evidence as well as introductory statements",
    " of editorial policy."
    #
    " But this review will only present detailed evidence of these claims regarding $BHQ Job.",
]
_CULT_OF_BHS = [
    "Like many students of Tanakh, I started out in the cult of $BHS.",
    #
    [" I thought $BHS was ", boj_html.bold("the")],
    " definitive edition.",
    #
    " Unlike many students of Tanakh, I eventually soured on $BHS,",
    " for the following reasons:",
]
#
_BHS_FAILS = [
    "It often fails to accurately transcribe μL (the Leningrad Codex).",
    #
    "It often fails to note where μL disagrees with other Tiberian manuscripts.",
    #
    "It emphasizes manuscript quantity over quality.",
]
_BHQ_AS_BHS_ALTERNATIVE = [
    "My first candidate for a $BHS alternative was $BHQ (Biblia Hebraica Quinta).",
    #
    " (Though I had soured on $BHS, I hadn’t escaped the broader cult of $DBG.)",
]
_SOURED = [
    "But I soon soured on $BHQ as well."
    #
    " I was dismayed to find that $BHQ will not be complete for many years.",
    #
    " More importantly, I found that $BHQ still suffers from some of the",
    " same problems as $BHS.",
    #
    " Although $BHQ now emphasizes manuscript quality over quantity,",
    " the other two problems listed above remain, albeit to a lesser degree.",
]
_BETTER_EDITIONS = [
    "I continued my search for better editions, and I found some.",
    #
    " This made me even more disappointed with $BHQ.",
    #
    " It seems to have been made in a bubble: its editors",
    " seem to have been unaware of or uninterested in",
    " relevant work done in other editions.",
    #
    " I can see why something like a fresh transcription of μL was beyond the scope of $BHQ.",
    #
    " But I can’t see why $BHQ would ignore the work already done in other editions,",
    #
    " in particular the following:",
]
_THE_THREE_EDITIONS = [
    [
        "The דעת מקרא (Da-at Miqra) series ($DM),",
        " particularly its",
        " “הנוסח ומקורותיו” sections",
        f" (Breuer et al., {num_range(1970, 2003)}).",
    ],
    [
        "Biblia Hebraica Leningradensia ($BHL),",
        " particularly its Appendix A ($BHL_A) (Dotan, 2001).",
    ],
    [
        "The Westminster Leningrad Codex ($WLC), particularly its notes",
        " (e.g. its ]1 and ]c notes),",
        " (editions dating back to the 1980s).",
    ],
]
_MEGILLOTH_2004 = [
    "The first fascicle of $BHQ (Megilloth) came out in 2004.",
    #
    " So, all three of the above editions were available to the $BHQ editors",
    " for all fascicles of $BHQ.",
]
_DM_PREDATES = [
    "All volumes of דעת מקרא predate $BHQ Megilloth."
    " Other works by Breuer are cited as sources in some fascicles of $BHQ,",
    " but the $BHQ editors",
    " seem to have been unaware of or uninterested in",
    " Breuer’s relevant work in דעת מקרא.",
]
_BHL_PREDATES = [
    "Dotan’s $BHL predates $BHQ Megilloth.",
    #
    " Dotan was even a consultant to the $BHQ project.",
    #
    " What’s more, his $BHL is cited as a source in many fascicles.",
    #
    " So it is puzzling that most of the $BHQ editors",
    " seem to have been unaware of or uninterested in",
    " his relevant work in $BHL_A.",
]
_AWARE_OF_BHL = [
    "The editors of some fascicles",
    " cite $BHL_A in their Introductions",
    " (Genesis, Leviticus, and Proverbs)."
    #
    " Though aware of it, they were not interested in it, at least not enough",
    " to have it deeply influence either the apparatus or the body text.",
    #
    " This represents a departure from the strictly diplomatic editorial policy of $BHS.",
    #
    " For better or for worse, $BHS aspired to transcribe (and often note) quirks in μL",
    " with almost no quirk deemed irrelevant,",
    " as long as it could be captured in print.",
    #
    " A good example is $BHS’s transcription of געיה before vowel marks.",
]
_WE_ARE_NOW_LEFT = [
    #
    "With $BHQ, we now have an edition that is unevenly diplomatic.",
    #
    " It still transcribes (and often notes)",
    " most or all of the quirks that $BHS editors found relevant,",
    " plus a smattering of new ones.",
    " But many quirks are not transcribed, and many that are transcribed are not noted.",
    #
    " In a few fascicles, we know that this unevenness is by design,",
    " as the editors refer the interested reader to $BHL_A",
    " for more information about the quirks in μL.",
    #
    " Perhaps all fascicles are uneven by design, i.e. uneven by editorial policy,",
    " and these are just the few that happen to document this policy.",
]
_JUDGES = [
    "Though it does not cite $BHL_A,",
    " $BHQ Judges is similarly explicit",
    " about its Masoretic limitations:",
    #
    " “Only those divergencies [of μL from consensus]",
    " that are meaningful for translation or exegesis",
    " have been noted in the apparatus.”",
    #
    " This is disappointing, but good to know, so that one can",
    " avoid $BHQ Judges if,",
    " for example, one’s interests include cantillation.",
    #
    " (Although cantillation quirks are common in μL,",
    " it is unlikely that any of them",
    " cause (or solve) some problem of translation or exegesis.)",
]
_WLC_PREDATES = [
    "$WLC has had various releases over its decades, many predating $BHQ Megilloth.",
    #
    " It is by far the most popular digital Hebrew Bible.",
    #
    " Plus, it is closely related to $BHS and $BHQ.",
    #
    " $WLC was originally a transcription of $BHS,",
    " and it carefully documents cases where it diverges from $BHS and/or $BHQ.",
    #
    " While $WLC “cares” a lot about $DBG Bibles,",
    " the reverse seems to be false since the $BHQ editors",
    " seem to have been unaware of or uninterested in",
    " $WLC, whose notes are particularly relevant to $BHQ.",
    #
    " This is puzzling since Alan Groves was intimately involved",
    " in both the $WLC and $BHQ projects.",
]
_MY_PURPOSES = [
    "Although it may already be clear, I should explicitly state that",
    " my purposes are narrowly focused on the Tiberian Masoretic text.",
    #
    " Thus I am not concerned with",
    " the many parts of $BHQ that deal with the following:",
]
_CLIST_NOT_MY_CONCERN = [
    "witnesses in languages other than Hebrew",
    "non-Tiberian Hebrew witnesses (e.g. unpointed ones)",
    "Masorah magna and parva (other than קרי Mp)",
    "the meaning of the text",
]
_CPARA_NOT_MY_CONCERN = [
    "For all I know, those parts of $BHQ are of high quality,",
    " representing the best modern scholarship on those topics.",
    #
    " But those parts are not my concern.",
]
_SPECIFICS_OF_BHQ_JOB = [
    "Having criticized $BHQ in general terms,",
    " I will now review the specifics of the $BHQ Book of Job (2024).",
    #
    " As of now (February 2026), it is the latest fascicle of $BHQ to be published",
    " and thus seems most relevant to review, if only one fascicle is to be reviewed.",
    #
    " I assume that $BHQ Job is at least broadly representative of the $BHQ series so far,",
    " although each fascicle has a different primary editor",
    " and may have different editorial teams working with that editor.",
]


def _contributions(the_len):
    return contributions_base("First, the good news: the", the_len)


_AFTER_CONTRIBUTIONS = [
    "Unsurprisingly, all of these contributions",
    " are new, i.e. not present in $BHS.",
    #
    " I find some of these proposed transcriptions",
    " far-fetched, e.g. unlikely to have been the scribe’s intention.",
    #
    " Nonetheless, I consider even those ones to be valuable contributions",
    " to the documentation of μL.",
]


def _reiterates_part1(the_len):
    return reiterations_base("It is also good news that the", the_len)


_COUNT_OF_RNTQ = 3  # RNTQ: reiterations new to BHQ
_DESCRIPTION_OF_RNTQ = [
    "three that are new are the ones in $link_6_21, $link_18_4_HLM3N5_2_of_2_FTW, and $link_19_16_QRAFY"
]
_WORDS_FOR_NUMBERS = {1: "one", 2: "two", 3: "three", 4: "four"}


_REITERATES_PART_2 = [
    " While a reiteration is not as valuable as a new contribution,",
    " it is still valuable.",
    #
    " Indeed my main criticism of $BHQ Job is that it",
    " should have reiterated most of what can be found in those other three editions.",
]


_CPARA_RNTQ = [
    "Unsurprisingly, all but",
    f" {_WORDS_FOR_NUMBERS[_COUNT_OF_RNTQ]}",
    " of the $BHQ reiterations",
    " are not new, i.e. they were already present in $BHS.",
    #
    " Indeed the other editions’ source may be $BHS in these cases.",
    #
    " Nonetheless we refer to all of them as reiterations by $BHQ.",
    #
    [" (The ", _DESCRIPTION_OF_RNTQ, ".)"],
    #
    " The reiterations made by $BHQ are as follows:",
]


def _reiterations(the_len):
    return [
        author.para(_reiterates_part1(the_len) + _REITERATES_PART_2),
        author.para(_CPARA_RNTQ),
    ]


def _bad_news_1(the_len):
    return [
        *bad_news_1_base("Now for some bad news: the", the_len),
        #
        " Not all such missing transcriptions are a bad thing,",
        " as the other editions may occasionally propose transcriptions that are",
        " far-fetched, e.g. unlikely to have been the scribe’s intention.",
        #
        " But overall these missing transcriptions reflect poorly on $BHQ Job.",
        #
        " In all but one case, a note is also lacking.",
        " (The one with a note is the one regarding %מאום in $link_31_7,",
        " although the note, too, is inaccurate.)",
    ]


def _after_bad_news_1_part_2(len_of_nbhq_and_n3):
    foo = len_of_nbhq_and_n3 - _COUNT_OF_RNTQ
    bar = len_of_nbhq_and_n3
    return [
        "As I said above, not all such missing transcriptions are a bad thing.",
        #
        " But the quirks not transcribed by $BHQ",
        " are of high quantity and high average quality.",
        #
        " This strongly suggests that $BHQ’s editors were either",
        " unaware of or uninterested in the other three editions.",
        #
        " I.e. it is unlikely that all these quirks were considered but rejected:",
        " it is more likely that they were simply not considered at all.",
        #
        f" This conclusion is strengthened by the fact that {foo} of the {bar}",
        " reiterations were already present in $BHS.",
        #
        f" The source of these {foo} reiterations is almost certainly $BHS,",
        " not one of the other three editions.",
    ]


_AFTER_BAD_NEWS_1_PART_3 = [
    "The failure to transcribe these quirks contrasts starkly"
    " with the $BHQ’s decision to continue and expand upon $BHS’s tradition of interest",
    " in Masorah notes, both parva and magna.",
    #
    " It is puzzling that an edition that is willing to devote so much effort (and space)",
    " to an area as obscure as Masorah notes is unwilling to devote similar or greater effort",
    " to improving the transcription accuracy of the pointing of its core text.",
]


def _implications(the_len):
    return [
        *implications_base("Now for some mixed news: the", the_len),
        #
        " We might say that in these cases $BHQ merely implies the quirk,",
        " because it is not explicit about it."
        #
        " (A note would be required to be explicit about it.)",
        #
        " Those quirks implied by $BHQ are as follows:",
    ]


_CONCLUSION = [
    "In conclusion, by using the other three editions, we find the following about $BHQ:",
]


def _conclusion_list(the_lens):
    len_wlc_dexi = the_lens["g:tbhq_and_zdw"]
    len_wlc_misc = the_lens["g:tbhq_and_zmw"]
    len_wlc_total = len_wlc_dexi + len_wlc_misc
    b = str(the_lens["g:nbhq_and_x3"])
    c = str(the_lens["g:nbhq_and_n3"])
    d = str(the_lens["g:tbhq_and_n3"])
    e = str(the_lens["g:xbhq_and_n3"])
    f = str(len_wlc_total)
    return [
        f"$BHQ contributes notes on {b} quirks not found in those editions.",
        f"$BHQ reiterates notes on {c} quirks found in those editions.",
        f"$BHQ transcribes but does not note {d} quirks found in those editions.",
        f"$BHQ does not transcribe {e} quirks found in those editions.",
        f"$BHQ transcribes but does not note at least {f} likely-false quirks.",
    ]


_POSTSCRIPT_UXLC = [
    "If $BHQ Job were being compiled today,",
    " $UXLC (a fork of $WLC) is another edition that could help.",
    " But $UXLC’s Job changes (and their accompanying notes)",
    " were made in 2022 and 2023,",
    " probably too late to be used by $BHQ.",
    " Nonetheless, $UXLC is an edition I would like to bring attention to.",
    " So, I would like to show the ways that $UXLC",
    " might contribute to $BHQ Job if it were being compiled today.",
    [" I do so in the ", d3_anchor()],
]
_POSTSCRIPT_QUIRKS_IN_MU_A = [
    "Usually, μA agrees with the consensus.",
    #
    " Indeed, where extant, it more or less ",
    boj_html.bold("defines"),
    " the consensus.",
    #
    " Nonetheless, there are cases where",
    " it is μA rather than μL that diverges from the consensus.",
    #
    " It is unclear what $BHQ Job’s policy is regarding such quirks in μA,",
    " but regardless of aspirational policy, in practice, I found no such notes in $BHQ Job.",
    #
    " To me, it would make sense for $BHQ to note them,",
    [" and therefore I note a few in the ", d4_anchor()],
]
_README = author.anc_h(
    "README",
    "https://github.com/bdenckla/document-index/blob/main/README.md",
)
_RELATED_WORKS_BY_ME = [
    "Other works by me about the Masoretic Text can be found in this",
    [" ", _README, "."],
]
