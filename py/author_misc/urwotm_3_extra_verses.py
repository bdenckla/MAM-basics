"""Exports gen_html_file.

Ported from the published Google Doc of the same title. The prose is
reproduced verbatim; the only deliberate changes are the ``$`` keys that
``dollar_sub`` requires, and the three intra-series links, which now point at
the sibling pages rather than at the Google Docs.
"""

from mb_author import author
from author_misc import urwotm_common


def anchor():
    return urwotm_common.anchor_part(3)


def gen_html_file(tdm_ch):
    cbody = [
        author.heading_level_1(urwotm_common.heading_1(_PART)),
        author.heading_level_2(urwotm_common.heading_2(_PART)),
        author.para(_PARA_002),
        author.unordered_list(urwotm_common.other_parts(_PART)),
        author.para(_PARA_004),
        author.para_for_img("urwotm/Josh 21v34-38 -- WLC schematic.png", width_em=22.7),
        author.para(_PARA_006),
        author.para_for_img("urwotm/Josh 21v34-38 -- L page 133B.png", width_em=44.4),
        author.para(_PARA_008),
        author.unordered_list(_LIST_009),
        author.para(_PARA_010),
        author.unordered_list(_LIST_011),
        author.para(_PARA_012),
        author.para_for_img("urwotm/Josh 21v34-38 -- L schematic.png", width_em=22.2),
        author.para(_PARA_014),
        author.para(_PARA_015),
        author.para(_PARA_016),
        author.unordered_list(_LIST_017),
        author.para(_PARA_018),
        author.para_for_img(
            "urwotm/Josh 21v34-38 -- BHS small type.jpg", width_em=131.3
        ),
        author.para(_PARA_020),
        author.para(_PARA_021),
        author.para(_PARA_022, {"class": "center"}),
        author.para(_PARA_023),
        author.para(_PARA_024, {"class": "center"}),
        author.para(_PARA_025, {"class": "center"}),
        author.para(_PARA_026, {"class": "center"}),
        author.para(_PARA_027),
        author.para(_PARA_028),
        author.para_for_img("urwotm/Josh 21v34-38 -- Aleppo.png", width_em=36.3),
        author.para(_PARA_030),
        author.para_for_img(
            "urwotm/Josh 21v35 את־דמנה -- Aleppo missing sof pasuq.png", width_em=25.9
        ),
        author.para(_PARA_032),
        author.para_for_img(
            "urwotm/Josh 21v34-38 -- Sassoon 1053 page 212.png", width_em=46.2
        ),
        author.para_for_img(
            "urwotm/Josh 21v34-38 -- Sassoon 1053 page 213.png", width_em=37.7
        ),
        author.para(_PARA_035),
        author.para_for_img(
            "urwotm/Josh 21v34 זבולן -- Sassoon 1053 cut off nun.png", width_em=16.9
        ),
        author.para(_PARA_037),
        author.para(_PARA_038),
        author.para(_PARA_039),
        author.para(_PARA_040),
        author.para(_PARA_041),
        author.para(_PARA_042),
        author.unordered_list(_LIST_043),
        author.para(_PARA_044),
        author.para(_PARA_045),
        author.unordered_list(_LIST_046),
        author.para(_PARA_047),
        author.para(_PARA_048),
        author.para(_PARA_049),
        author.para_for_img(
            "urwotm/Josh 21v36-37 -- UXLC gray setumah.png", width_em=43.7
        ),
        author.para(_PARA_051),
        author.blockquote(_QUOTE_052),
        author.para(_PARA_053),
        author.para_for_img("urwotm/Josh 21v36 -- JPS HET asterisk.png", width_em=26.7),
        author.para(_PARA_055),
        author.para_for_img("urwotm/Josh 21v36 -- JPS HET note.png", width_em=30.5),
        author.para(_PARA_057),
        author.para(_PARA_058),
        author.para(_PARA_059),
        author.para_for_img("urwotm/Josh 21v35 -- BHL note.png", width_em=52.5),
        author.para(_PARA_061),
        author.para(_PARA_062),
        author.para(_PARA_063),
        author.para(_PARA_064),
        author.para_for_img(
            "urwotm/Josh 21v36-37 -- Zondervan RHB.png", width_em=131.3
        ),
        author.para(_PARA_066),
    ]
    return author.help_gen_html_file(__file__, tdm_ch, _FNAME, _TITLE, cbody)


_PART = 3
_TITLE = urwotm_common.plain_title(_PART)
_FNAME = urwotm_common.FNAMES[_PART]

_PARA_002 = """This is the third article in a series. The series is about errors in $BHS and/or
$WLC. The other articles in the series are as follows:""".replace(
    "\n", " "
)
_PARA_004 = """In editions close to $WLC, such as Accordance HMT-W4 and Logos LHB, Joshua 21:34–38
look, schematically, like this:""".replace(
    "\n", " "
)
_PARA_006 = """But ל has no content corresponding to $WLC’s verses 36 and 37! Page 133B, column 1,
lines 4–11 of ל look like this (highlighting added of course):""".replace(
    "\n", " "
)
_PARA_008 = "It all starts out fine. In ל we see:"
_LIST_009 = [
    "a $setumah paragraph break",
    "content corresponding to $WLC’s verses 34 and 35",
]
_PARA_010 = "But right after that, we see:"
_LIST_011 = [
    "a $setumah paragraph break",
    "content corresponding to $WLC’s verse 38!",
]
_PARA_012 = "Schematically, ל looks like this:"
_PARA_014 = """In other words, in ל we go straight from the tribe of Zebulun to the tribe of Gad.
No Reuben.""".replace(
    "\n", " "
)
_PARA_015 = """These “missing” verses are not an idiosyncrasy of ל. And even if they were, $WLC is
supposed to be a strictly diplomatic edition of ל, so if ל lacks these verses, $WLC
should lack these verses. What’s going on here?""".replace(
    "\n", " "
)
_PARA_016 = """$WLC did not start with the goal of representing ל. $WLC started with the goal of
representing a subset of $BHS. That subset consists of:""".replace(
    "\n", " "
)
_LIST_017 = [
    "the $BHS body text",
    "the $BHS notes relating to $qere and/or $ketiv",
]
_PARA_018 = [
    "Though $WLC did evolve to have some corrections to $BHS, it still remained",
    " quite close to $BHS. So, what does $BHS look like here? The answer is that",
    " $BHS has these verses 36 and 37, ",
    author.emphasis("but they are in smaller type!"),
]
_PARA_020 = """So $WLC transcribes $BHS too abstractly here: it abstracts away the change in type
size. The proper way to have transcribed $BHS here probably wouldn’t have been to
mark these verses as small, per se: that’s too concrete. But they should have been
marked as something like “interpolated” or “not in ל”. In other words, the change in
type size should have been abstracted, but not abstracted away!""".replace(
    "\n", " "
)
_PARA_021 = """Although the $BHS apparatus is normally irrelevant to the task of the $WLC
transcriber, here the small type should have been a clue that something was going on
that was worth looking into. The small type should have led them to look at
apparatus note “a” in (pseudo) verse 36. It starts with the following notation,
which records what I wish they had found a way to record in $WLC:""".replace(
    "\n", " "
)
_PARA_022 = "v 36.37 > $LC"
_PARA_023 = [
    "Here “$LC” means not only the Leningrad Codex but also the Cairo Codex of the",
    " Prophets. I.e. $LC is short for “",
    author.emphasis("L"),
    "[eningrad Codex] and ",
    author.emphasis("C"),
    "[airo Codex of the Prophets]” not “",
    author.emphasis("L["),
    "eningrad] ",
    author.emphasis("C["),
    "odex].” With that, we can decode “v 36.37 > $LC” to mean:",
]
_PARA_024 = "Verses 36 through 37"
_PARA_025 = "are an addition relative to (i.e. do not appear in)"
_PARA_026 = "the Leningrad Codex and the Cairo Codex of the Prophets."
_PARA_027 = """L and C are the only Hebrew manuscripts cited, i.e. they cite no contradictions to
this tradition. Indeed I doubt there are any among the other esteemed manuscripts,
two of which I will review below: א and ש1. Though scholars (and amateurs such as
me) love to study differences within the Masoretic tradition, we must admit, when we
“come up for air” and get some perspective, that these differences are, though
numerous, minute. I am not aware of any differences as large as a word missing, much
less two verses.""".replace(
    "\n", " "
)
_PARA_028 = """Here’s the relevant passage from the Aleppo Codex (א) (page ?, column 2, lines 4–11)
(from Bar-Ilan images):""".replace(
    "\n", " "
)
_PARA_030 = """As an aside, note that there is a $sof_pasuq mark missing in the excerpt from א
above, i.e. the colon-shaped mark shown in red below is missing just before the
highlighted compound את־דמנה:""".replace(
    "\n", " "
)
_PARA_032 = """Here’s the relevant passage from Sassoon 1053 (aka ש1 aka שׂ ($sin)) (page 212,
column 3, last 5 lines; page 213; column 1, first 2 lines) (from IHBMR images):""".replace(
    "\n", " "
)
_PARA_035 = """As an aside, note that the final $nun of זבולן is cut off. (זבולן is one of our
highlighted keywords.) I think this $nun might be cut off not only in the photo, but
in the actual artifact. There appears to be some sort of joint near the gutter, but
this joint is not the source of the problem; indeed the $lamed of זבולן is written
“after” this joint. The real problem, I think, is that there wasn’t enough space
even with writing “after” the joint. There is a thin vertical line after the $lamed
that might be part of this $nun. But I am not sure that this line is made by ink.
There are other lines somewhat like it above, near the gutter. Here’s a higher-res
detail of this word and its environs, without highlighting interfering (thanks to
Dr. Nehemia Gordon for supplying this image):""".replace(
    "\n", " "
)
_PARA_037 = "Emerging from this digression on זבולן in ש1, where are we?"
_PARA_038 = """We have shown that two other esteemed manuscripts, א and ש1, agree with the two
manuscripts already cited by $BHS (L and C) (aka ל and ק).""".replace(
    "\n", " "
)
_PARA_039 = """It seems likely that at some point in the development of the Hebrew Bible, somebody
accidentally omitted these two verses about the transfer of four towns from the
tribe of Reuben. (These towns were transferred to the Merarite clan of the Levites).
The idea that this is an omission is strongly supported by a parallel passage in 1
Chronicles 6, since these Reuben towns are listed there.""".replace(
    "\n", " "
)
_PARA_040 = """Even though it is likely that these two verses “should be there” in some sense, this
is irrelevant to the Masoretic project. They still should not be there, in a
Masoretic sense.""".replace(
    "\n", " "
)
_PARA_041 = """Likely someone accidentally omitted these two verses in some influential text, and
that text, with that omission, is the one that became Masoretically canonical. In
this sense the only mistakes in Masoretic manuscripts are where manuscripts disagree
with one another. Sometimes it is difficult to say, in such cases, which manuscripts
are right, and which are wrong, but fortunately that is not the case here. At least
in the four manuscripts we have discussed, there is total agreement. And these are
not just any four manuscripts, these are arguably the four most important
manuscripts to consult, for the book of Joshua.""".replace(
    "\n", " "
)
_PARA_042 = """When we publish a Masoretic Hebrew Bible, our task is easier than related tasks such
as publishing a translation. A translation likely draws on multiple sources,
including pre-Masoretic Hebrew sources (Qumran) as well as sources in Aramaic,
Syriac, and/or Greek. Here in Joshua 21 we can see that, with the use of small type,
the $BHS editors tried to balance two almost-incompatible goals for $BHS:""".replace(
    "\n", " "
)
_LIST_043 = [
    "Be a diplomatic edition of ל",
    [
        "Be a wide-ranging, multi-language critical edition of the Hebrew Bible,",
        " oriented towards tasks such as translation",
    ],
]
_PARA_044 = """$WLC should have omitted these verses or found a way to mark them with a semantic
equivalent to $BHS’s small type. Instead, $WLC, supposedly only a diplomatic edition
of ל, became polluted with two verses only relevant to a wide-ranging,
multi-language critical edition of the Hebrew Bible.""".replace(
    "\n", " "
)
_PARA_045 = """A small problem related to a $setumah break is embedded within $WLC’s larger
mistake. $WLC represents a $setumah break as an “S” marker at the end of the verse
preceding the break. (This “S” marker is often rendered as a $samekh (ס) in printed
editions.) The “ownership” of a $setumah or $petuxah marker is always a tricky issue
in representing the Hebrew Bible in a dataset. Does such a marker:""".replace(
    "\n", " "
)
_LIST_046 = [
    "“belong” to the verse that precedes the marker?",
    "“belong” to the verse that follows the marker?",
    "“belong” to neither?",
]
_PARA_047 = """As always, there are advantages and disadvantages to each of those three approaches.
But, I think that the best compromise is to have such a break “belong” neither to
the verse that precedes it nor to the verse that follows it.""".replace(
    "\n", " "
)
_PARA_048 = """One disadvantage of $WLC’s choice to have a $setumah marker belong to the preceding
verse is that this makes a Masoretic $setumah break “belong” to non-Masoretic verse
37. So an edition close to $WLC can’t correct $WLC’s error by simply dropping verses
36 and 37: it must “rescue” the $setumah break “taken hostage” by verse 37.""".replace(
    "\n", " "
)
_PARA_049 = """For example, though, commendably, $UXLC corrects $WLC’s error by marking these
verses with an “X” and showing them in gray, the astute observer may notice that the
$samekh of this $setumah break gets “swept up” in the grayness, making this $setumah
break look non-Masoretic:""".replace(
    "\n", " "
)
_PARA_051 = """$WLC’s failure to mark these verses is partially addressed in version 4.22, with the
following comment in its header:""".replace(
    "\n", " "
)
_QUOTE_052 = """NOTE: This file includes Joshua 21:36-37, just as previous versions have always
done. Those two verses are *not* found in the Leningrad Codex (or in the Aleppo
Codex or in most early codices) but *are* found in later manuscripts and printed
editions of the Hebrew Bible.""".replace(
    "\n", " "
)
_PARA_053 = """We conclude by noting how this issue is handled in important printed editions. In
the $JPS HET an asterisk appears before the verse number label for verse 36:""".replace(
    "\n", " "
)
_PARA_055 = "This asterisk leads to the following note:"
_PARA_057 = """(כאן נתחבר שני פסוקים במהדורת שטוטגרט על פי נוסח אחר, אז בשאר הפרק גורמים לשינוי
פסוקים כנספר)""".replace(
    "\n", " "
)
_PARA_058 = """This note means, roughly, “here we skip two verses in $BHS in order to conform to
another tradition, so in the rest of this chapter our verse numbers differ [from
those of $BHS].”""".replace(
    "\n", " "
)
_PARA_059 = "In Dotan’s BHL, the following appears at the bottom of the relevant page:"
_PARA_061 = (
    "(“A few other manuscripts include two additional verses after verse 35 [...]”)"
)
_PARA_062 = """(I’m curious as to whether any of the manuscripts Dotan refers to are esteemed
Masoretic ones.)""".replace(
    "\n", " "
)
_PARA_063 = [
    author.book_title("Keter Yerushalayim"),
    " makes no such “apology” for its “missing” verses.",
]
_PARA_064 = [
    "Zondervan’s RHB (",
    author.book_title("A Reader’s Hebrew Bible"),
    ") (Brown & Smith), though strictly based on $WLC 4.4, commendably supplements",
    " its $WLC base text with some big square brackets and a change to a smaller",
    " font size as in $BHS:",
]
_PARA_066 = """(Note that $WLC 4.4 is not, as it might seem, more recent than the most recent $WLC,
version 4.22, which was released in November of 2020. The dot used in $WLC versions
separates the major and minor revision integers, not the integer and fractional
parts of a number expressed in decimal notation. In short, $WLC 4.4 might be called
$WLC 4.04 in a different versioning scheme.)""".replace(
    "\n", " "
)
