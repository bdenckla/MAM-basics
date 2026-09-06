"""Exports gen_html_file.

Ported from the published Google Doc of the same title. The prose is
reproduced verbatim; the only deliberate changes are the ``$`` keys that
``dollar_sub`` requires, and the three intra-series links, which now point at
the sibling pages rather than at the Google Docs.
"""

from mb_misc import mb_html
from mb_author import author
from author_misc import urwotm_common


def anchor():
    return urwotm_common.anchor_part(1)


def gen_html_file(tdm_ch):
    cbody = [
        author.heading_level_1(urwotm_common.heading_1(_PART)),
        author.heading_level_2(urwotm_common.heading_2(_PART)),
        author.para(_PARA_002),
        author.unordered_list(urwotm_common.other_parts(_PART)),
        author.para(_PARA_004),
        author.para_hbo(_HBO_005),
        author.para(_PARA_006),
        author.para(_PARA_007),
        author.unordered_list(_LIST_008),
        author.para(_PARA_009),
        author.para(_PARA_010),
        author.para(_PARA_011),
        author.para_hbo(_HBO_012),
        author.para(_PARA_013),
        author.para(_PARA_014),
        author.para(_PARA_015),
        author.para(_PARA_016),
        author.para(_PARA_017),
        author.para_for_img("urwotm/Deut 12v30 לאמר -- L color.png", width_em=42.4),
        author.para(_PARA_019),
        author.unordered_list(_LIST_020),
        author.para(_PARA_021),
        author.para_for_img("urwotm/Deut 12v30 לאמר -- BHS.png", width_em=29.6),
        author.para(_PARA_023),
        author.para(_PARA_024),
        author.para_for_img(
            "urwotm/Deut 12v30 לאמר -- L black and white.png", width_em=30.6
        ),
        author.para(_PARA_026),
        author.para(_PARA_027),
        author.unordered_list(_LIST_028),
        author.para(_PARA_029),
        author.para(_PARA_030),
        author.para(_PARA_031),
        author.para(_PARA_032),
        author.para(mb_html.code(_CODE_033), {"class": "center"}),
        author.para(_PARA_034),
        author.para(_PARA_035),
        author.para(_PARA_036),
        author.para(_PARA_037),
        author.para(_PARA_038),
        author.para(_PARA_039),
        author.para(_PARA_040),
        author.para(_PARA_041),
        author.para(_PARA_042),
        author.para_for_img("urwotm/Deut 12v30 לאמר -- BHQ.png", width_em=32.3),
        author.para(_PARA_044),
        author.para(_PARA_045),
        author.para_for_img("urwotm/Deut 12v30 לאמר -- JPS HET.png", width_em=14.2),
        author.para(_PARA_047),
        author.para(_PARA_048),
        author.unordered_list(_LIST_049),
        author.para(_PARA_050),
        author.para_for_img("urwotm/Deut 12v30 לאמר -- Sassoon 507.png", width_em=19.2),
        author.para(_PARA_052),
        author.unordered_list(_LIST_053),
        author.para(_PARA_054),
        author.para(_PARA_055),
        author.para_for_img(
            "urwotm/Deut 12v30 לאמר -- Sassoon 1053.png", width_em=41.6
        ),
        author.para(_PARA_057),
        author.para(_PARA_058),
        author.para(_PARA_059),
        author.para_for_img("urwotm/Deut 12v30 לאמר -- URJ ḥumash.png", width_em=12.2),
        author.para(_PARA_061),
        author.para(_PARA_062),
        author.para(_PARA_063),
        author.para(_PARA_064),
        author.para(_PARA_065),
        author.unordered_list(_LIST_066),
    ]
    return author.help_gen_html_file(__file__, tdm_ch, _FNAME, _TITLE, cbody)


_PART = 1
_TITLE = urwotm_common.plain_title(_PART)
_FNAME = urwotm_common.FNAMES[_PART]

_URL_TANACH_US_1 = (
    "https://tanach.us/Changes/2020.10.19%20-%20Changes/2020.10.19%20-%"
    "20Changes.xml?2020.09.22-1"
)
_URL_IHBMR_COM_1 = "https://ihbmr.com/"
_URL_BDENCKLA_GITHUB_IO_1 = (
    "https://bdenckla.github.io/MAM-basics/MAM-with-doc/A5-Deuter.html#c12v30"
)
_URL_TANACH_US_2 = (
    "https://tanach.us/Changes/2020.02.19%20-%20Changes/2020.02.19%20-%"
    "20Changes.xml?2019.09.01-1"
)

_PARA_002 = """This is the first article in a series. The series is about errors in $BHS and/or
$WLC. The other articles in the series are as follows:""".replace(
    "\n", " "
)
_PARA_004 = """In many popular editions of the Hebrew Bible, Deut. 12:30’s לאמר is accented with a
$qadma on its $mem, as shown below:""".replace(
    "\n", " "
)
_HBO_005 = "לֵאמֹ֨ר"
_PARA_006 = "There’s nothing remarkable about this, except that it is wrong."
_PARA_007 = "We will investigate the following:"
_LIST_008 = [
    "Which editions get this wrong, and why?",
    "Which editions get this right, and why?",
    "Which editions got this wrong, but have been corrected?",
]
_PARA_009 = """Answering these questions for this particular case will yield general insights into
the ongoing project of standardization and preservation of the Hebrew Bible. As
scrolls from Qumran show, this project did not start with the Masoretes. But this
project achieved great maturity under their stewardship. As we moved from their
handwritten codices to printed and digital editions, both corrections and errors
came to be propagated more faithfully and widely than ever before.""".replace(
    "\n", " "
)
_PARA_010 = """It is the continuing responsibility of each generation of stewards (scholars and
publishers) to make sure that, on balance, corrections outnumber errors. Only in
this way can we preserve at least the degree of standardization that the Masoretes
achieved. This seems like it should be easy for us, given the technologies we have
at our disposal. Yet, this goal has proved difficult to achieve, and at this point
in time, I am unclear who is winning, the errors or the corrections.""".replace(
    "\n", " "
)
_PARA_011 = """Getting back to the particular case, why do I make the bold claim that this $qadma
is wrong? Usually I would couch my judgments about an edition of the Hebrew Bible in
less extreme terms, e.g. “unlikely to have been the intention of the scribe” rather
than “wrong.” But this situation is extreme. First of all, a $qadma doesn’t make
sense here, in context:""".replace(
    "\n", " "
)
_HBO_012 = "לאמ֨ר איכ֨ה יעבד֜ו"
_PARA_013 = """This would be the only case in the Hebrew Bible in which a $qadma is followed
immediately by another $qadma, i.e. with no intervening accent. On the other hand,
lots of things happen only once in the Hebrew Bible. So, this accent can’t be deemed
wrong just because it contradicts what we (think we) know about the grammar of
accents. But, this accent’s contradiction of grammar should certainly make us
suspicious, and send us looking for evidence in as many reputable manuscripts as
possible.""".replace(
    "\n", " "
)
_PARA_014 = """I should add that, for all we know at this point in the story (in the way I’m
choosing to tell this story) maybe it is this accent’s context that is wrong, not
this accent itself! Or, again, maybe nothing’s wrong with either this accent or its
context. In that case, the only thing wrong is our grammar of accents, which needs
to be updated to accept this exception. The bottom line is, we need to consult some
manuscripts.""".replace(
    "\n", " "
)
_PARA_015 = """First let’s consult the Leningrad Codex (henceforth ל). If we find that ל has a
$qadma, that is important to know, but that fact alone would not vindicate editions
having $qadma. It would merely mean that they agree with ל. It is a common mistake
to believe that agreement with ל constitutes correctness. It only constitutes
correctness for a strictly diplomatic edition of ל, like $BHS.""".replace(
    "\n", " "
)
_PARA_016 = """(No strictly diplomatic edition of ל should be popular, because such an edition
should be of scholarly interest only. Unfortunately, in practice, this is not the
case. $BHS and its close derivatives are very popular. I would even say that they
are not just popular but dominant within certain contexts. I cannot fault $BHS for
becoming popular, but I can fault its users (including the publishers of close
derivatives) for making it popular by putting it to use in ways that are
inappropriate or misleading.)""".replace(
    "\n", " "
)
_PARA_017 = """The preceding ideological tangent is, fortunately, irrelevant to the case at hand
since inspection of the color image of the relevant page of ל reveals that the
accent is not $qadma, as can be seen below.""".replace(
    "\n", " "
)
_PARA_019 = """The quality of the image and the quality of the text here are both high enough to
establish, with high confidence, that the $mem in question has two above-marks,
which are, from right to left, a $revia dot and a $xolam dot. The $xolam dot has two
non-ideal properties, which we list below.""".replace(
    "\n", " "
)
_LIST_020 = [
    [
        "The $xolam dot is very close to, indeed almost touching, the “horn” of the",
        " $mem.",
    ],
    [
        "The $xolam dot is somewhat ellipse-like, with a roughly",
        " southeast-to-northwest axis.",
    ],
]
_PARA_021 = """The above two non-ideal properties of the $xolam dot are where all the confusion
lies about this word. Here’s what the 1997 (most recent) $BHS has, though I suspect
this error predates the 1997 edition:""".replace(
    "\n", " "
)
_PARA_023 = [
    "$BHS chooses to interpret these two marks in ל as, right to left, an oddly",
    " “early” $xolam dot followed by an “illegal” $pashta. It is important to note",
    " that this $pashta is “illegal” according to the ",
    author.emphasis("intra"),
    "-word grammar of accents, not the ",
    author.emphasis("inter"),
    "-word grammar mentioned above. In particular, $pashta is supposed to be a",
    " postpositive accent, which means that in cases like this, where there is only",
    " one $pashta on a word, that $pashta is constrained to be above (and usually",
    " “late” on) the last letter of that word. So in this case we would expect",
    " $pashta to be above and late on $resh, not above and late on $mem (or above",
    " and early on $resh).",
]
_PARA_024 = """The following black and white image sheds some light on why $BHS may have made this
error:""".replace(
    "\n", " "
)
_PARA_026 = """This image is probably worse than what $BHS editors had access to, but its lack of
color and its low resolution are probably illustrative of the source of the
confusion. (We assume that the $BHS editors did not have access to color images, and
I’m unsure whether they had access to high-resolution images.)""".replace(
    "\n", " "
)
_PARA_027 = """While the $BHS editors’ mistake is unfortunate, they made a commendable effort to
represent, in type, something close to what they (thought they) were seeing. I don’t
know whether the particular person responsible for this transcription knew that such
a use of $pashta was “illegal.” Even if they knew it was illegal:""".replace(
    "\n", " "
)
_LIST_028 = [
    [
        "They probably were also well aware that lots of things happen only once in",
        " the Hebrew Bible, i.e. “expected illegalities” are not unheard of. So there’s",
        " good reason to resist the impulse to harmonize a word with (what you view as)",
        " its analogs elsewhere.",
    ],
    [
        "As transcribers of a strictly diplomatic edition of ל, their job was to",
        " transcribe ל, not correct ל. On the other hand, $BHS is not only a strictly",
        " diplomatic edition of ל, it is also a critical edition, which should be",
        " expected to note cases in which ל has unexpected (or even “illegal”)",
        " contents. So perhaps we can’t fault the $BHS editors for this mistake in",
        " transcription, but I think it is fair to fault them for not noting the result",
        " as “illegal.”",
    ],
]
_PARA_029 = """Note that though the $BHS editors tried to represent the precise location of the
accent, they “sanitized” the location of the $xolam dot. This is all part of the
delicate job of a transcriber: to abstract away some details of the manuscript,
while retaining others. These decisions depend somewhat on the judgment of the
transcriber but depend on the technology being transcribed to. So, for example, for
all I know, an “early” $xolam was desired by the transcriber, but could not be
realized since it was too hard to typeset.""".replace(
    "\n", " "
)
_PARA_030 = """Now we can trace (or at least speculatively trace) the propagation of this error
from $BHS to other editions, across the decades. (It would be interesting to see how
far back in $BHS’ history this error goes, but it is beyond the scope of this study
to do so. As I mentioned, I speculate that this error exists in editions of $BHS
long prior to 1997.)""".replace(
    "\n", " "
)
_PARA_031 = """Interestingly, this error was not propagated faithfully. It remained an error, i.e.
it was not corrected, but this $pashta became a $qadma at some point. $Qadma is
still an error, since the accent on $mem should be a $revia, but it is a different
error.""".replace(
    "\n", " "
)
_PARA_032 = """My guess is that the $BHS $pashta became a $qadma during the transcription of $BHS
to digital form in the Michigan-Claremont Westminster text, later known as the
Westminster Leningrad Codex ($WLC). In detail, this word became:""".replace(
    "\n", " "
)
_CODE_033 = 'L " / ) M O 63 R'
_PARA_034 = """These codes mean, respectively, $lamed (L), $tsere ("), morphology division (/),
$alef (closing parenthesis), $mem (M), $xolam dot (O), $qadma (63), and $resh (R).
In $WLC 4.22, the most recent release of $WLC as of this writing, the accent has
been fixed to be $revia. The word is now L"/)MO81R (note “81” as opposed to “63”).
But, I will continue to discuss the erroneous version of this word that appears in
$WLC 4.20 and previous versions, because unfortunately 4.22 has had little “take-up”
as of yet, and the mistake in previous versions of $WLC has already propagated to
many paper editions.""".replace(
    "\n", " "
)
_PARA_035 = """My guess is that the mark I am calling “$BHS’s $pashta” was interpreted by the $WLC
transcriber not as a $pashta located in a strange place within the word but as a
$qadma located in a reasonable place within the word but in a strange micro-location
in relation to its letter ($mem). In other words, the $WLC transcribers interpreted
this mark in $BHS as an oddly late-on-the-$mem $qadma rather than an oddly
early-in-the-word $pashta. $BHS had the luxury (or pitfall) of transcribing such a
mark ambiguously, because, on paper, no such distinction can be made between these
two interpretations of the mark. (That is, no such distinction can be made, given
that $BHS’s font makes no distinction between the shape of $pashta and $qadma).""".replace(
    "\n", " "
)
_PARA_036 = """$WLC has no such luxury of ambiguity; its representation is an abstract one in which
$pashta or $qadma must be chosen. Given that $WLC has no way to qualify a $qadma as
“late,” if the transcriber of $BHS feels that this mark is a “late” $qadma in $BHS,
the transcriber must, logically, drop the “late” part but retain the identity of
$qadma. (It is perhaps interesting to note that $WLC followed $BHS in painstakingly
preserving three “flavors” of $meteg (aka $gaya_with_half_ring_for_ayin): early,
middle, and late. No modern scholar I am aware of maintains that these distinctions
are meaningful, but perhaps this was not well-established in the 1970s when $BHS was
first completed.)""".replace(
    "\n", " "
)
_PARA_037 = [
    "It is an important rule of transcription to a dataset (observed here by $WLC",
    " but often violated elsewhere) that one not use the wrong accent to mimic the",
    " right position, in pairs of accents that look similar in most fonts, like",
    " $pashta and $qadma. This is a major difference in the requirements for the",
    " digital encoding of texts intended merely for printing as opposed to the",
    " digital encoding of texts intended for use as a dataset, i.e. intended for",
    " use in a variety of (probably unknown) ways. A text meant only to be printed",
    " on paper (or displayed on a website) in a known font can “cheat” (either by",
    " accident or on purpose) and do anything underneath in the encoding that ends",
    " up looking right (or looking close enough to right) when printed or",
    " displayed. This is decidedly not true of a dataset. Here is an example of ",
    author.anc_h("a change in Leviticus 1:3", _URL_TANACH_US_1),
    " that I proposed to $UXLC (later accepted) involving another pair of accents",
    " that look similar in most fonts, $geresh and $germuq.",
]
_PARA_038 = """$WLC itself used to “cheat” by using the code for $qadma (63) to represent the first
of two $pashta marks on a word, when a word has two such marks. (I usually refer to
this first mark as the “stress-helper” $pashta, but there is no standard term for
this first $pashta.) Then at some point $WLC introduced a new, dedicated accent
code, 33, for stress-helper $pashta. This development is laudable, and I wish
Unicode had an analogous code point.""".replace(
    "\n", " "
)
_PARA_039 = """Unicode texts either “cheat” and use $qadma or they use $pashta both for the primary
(i.e. final) mark and the stress-helper mark. This second strategy, using $pashta in
both places, is preferable to “cheating,” but it is still not ideal since it places
a burden on every font supporting Biblical Hebrew. The font is burdened because it
must determine, from context, which of the two types of $pashta it should display.
Most fonts need to distinguish the two types of $pashta because most fonts “want” to
position the stress-helper $pashta centrally. I.e. they “want” to position it more
like a $qadma.""".replace(
    "\n", " "
)
_PARA_040 = """In contrast, $BHS does not position the stress-helper $pashta centrally. Indeed the
$WLC documentation specifies that accent 33, stress-helper $pashta, represents a
$pashta written “after the letter not over it (unlike the [$qadma]).” This reflects
$WLC’s original (and still primary) role as a transcription of $BHS, not of ל. I am
not aware of any study of the position of stress-helper $pashta in ל, in my
experience, it is roughly central or at a minimum, inconsistent.""".replace(
    "\n", " "
)
_PARA_041 = """So, in $WLC, this word might have been re-coded from 63 ($qadma) to 33
(stress-helper $pashta) when 33 was introduced. This would have more accurately
reflected the contents of $BHS, and would have been “less illegal” than a primary
$pashta (03) since a primary $pashta should never appear on a non-final letter. The
word as a whole would have still been illegal since any word with a stress-helper
$pashta should also have a primary $pashta. And in any case, whether 03, 33, or 63
were used, the word would still not represent the contents of ל.""".replace("\n", " ")
_PARA_042 = """In 2007, $BHQ, the still-in-progress successor to $BHS, put this mark in the
standard location for $qadma: centered above the $mem. Whether $BHQ did this
independently of $WLC or because of $WLC, I don’t know.""".replace(
    "\n", " "
)
_PARA_044 = [
    "$BHQ’s treatment of this word is arguably worse than $BHS’s, since $BHS,",
    " though in error, at least looks weird, giving the reader a clue that",
    " something weird is going on. $BHQ “sanitizes” $BHS’s error away. We are left",
    " with only the odd ",
    author.emphasis("inter"),
    "-word grammar (two $qadma marks in a row) as a clue as opposed to $BHS where",
    " we have odd ",
    author.emphasis("intra"),
    "-word grammar (oddly-late-on-its-letter $qadma or oddly-early-in-its-word",
    " $pashta). I.e. in $BHS, the word itself gives us a clue that something fishy",
    " may be going on.",
]
_PARA_045 = """Jumping back from 2007 to 2000, $JPS’s Hebrew-English Tanakh (HET), like $BHQ, has a
normally-positioned $qadma:""".replace(
    "\n", " "
)
_PARA_047 = """It is not surprising that the HET has this since though its Hebrew text is a
heavily-corrected version of $WLC, most of its corrections come from sources
identifying anomalies in ל, not errors in $BHS or $WLC. And those sources, such as
the work of Breuer and Dotan, do not comment upon this word, presumably because,
even though I think they lacked access to color images, they gave the marks on the
$mem the unremarkable interpretation of $revia and $xolam respectively, from right
to left.""".replace(
    "\n", " "
)
_PARA_048 = """This word appears incorrectly in all editions close to $WLC, such as these two
notable digital ones:""".replace(
    "\n", " "
)
_LIST_049 = [
    "Logos LHB (Lexham Hebrew Bible)",
    "Accordance HMT-W4",
]
_PARA_050 = """Let’s look at this word in the Damascus Pentateuch aka Sassoon 507 (page 404, column
3, last line):""".replace(
    "\n", " "
)
_PARA_052 = """The text is not in great shape here but it is of sufficient quality to confirm, with
high confidence, the $revia and $xolam dots over the $mem. The bullet list below
contains some additional remarks on this image. (I allow myself these digressions
since part of my aim here is to highlight some general issues in manuscript
transcription.)""".replace(
    "\n", " "
)
_LIST_053 = [
    [
        "As is usually the case, instead of saying that the $xolam dot is over the",
        " $mem, one could say that it is over and between the $mem and the $resh, but",
        " “ownership” is not important here.",
    ],
    [
        "There is a small but dark dot just above the $revia dot. I assume it is not",
        " ink, or in any case not intentional.",
    ],
    [
        "Unlike in ל, here there is a $rafeh bar above the $alef, presumably",
        " emphasizing that the $alef is here merely a ",
        urwotm_common.romanized("mater lectionis"),
        " corresponding to the $tsere vowel, not a (glottal stop) consonant.",
    ],
]
_PARA_054 = """What does it mean for one or more manuscripts to confirm our reading of ל? The
answer is pretty clear for an eclectic edition of the Hebrew Bible, but the answer
is less clear, i.e. the question is more interesting, for an ל-diplomatic edition.
For that more interesting case, the question becomes: to what extent should we allow
our transcription of ל to be influenced by what we find in other manuscripts? There
is no clear-cut answer. The impulse to harmonize is strong, not only to harmonize
within a manuscript but also between manuscripts. While there’s good reason to
resist this impulse, the impulse is not wrong per se. With respect to accents for
example, it is clear that these manuscripts arise from a highly standardized
chanting tradition. So while we should not stretch too far to see ל match as
matching other manuscripts, neither should we insist that a word be interpreted
without influence from other manuscripts.""".replace(
    "\n", " "
)
_PARA_055 = [
    "Let’s look at this word in a third manuscript, Sassoon 1053 (recently sold",
    " for ",
    mb_html.raw_html("$"),
    "38.1 million) (page 168, column 3, line 1):",
]
_PARA_057 = [
    "(Apologies for cutting off the luxuriantly-long ascender of the $lamed but it",
    " seemed impractical to include it.) (Thanks to the ",
    author.anc_h("Institute for Hebrew Bible Manuscript Research", _URL_IHBMR_COM_1),
    " for providing these images in indexed form, making it easy to find which",
    " image contains a given verse.)",
]
_PARA_058 = """The image confirms, with high confidence, the $revia and $xolam dots over the $mem.
(There is a light brown dot above the left “arm” of the $alef; I consider it not
ink, or in any case not intentional.)""".replace(
    "\n", " "
)
_PARA_059 = "The word appears correctly in the 2005 URJ $xumash:"
_PARA_061 = [
    "It appears correctly in Dotan’s BHL, in the ",
    author.book_title("Keter Yerushalayim"),
    ", and in editions by Koren and Simanim.",
]
_PARA_062 = [
    "This word appears correctly in $MAM, a liberally-licensed dataset of the",
    " Hebrew Bible used in various editions. Characteristically, it is not only",
    " correct in $MAM, but ",
    author.anc_h(
        "the error in other editions is documented in $MAM", _URL_BDENCKLA_GITHUB_IO_1
    ),
    ".",
]
_PARA_063 = """This error is an example of a general pattern in which it seems that the best way to
avoid the long shadow of $BHS errors is to use editions made in Israel, where $BHS’s
influence seems to be far less than elsewhere.""".replace(
    "\n", " "
)
_PARA_064 = [
    "This error was ",
    author.anc_h("corrected in $UXLC", _URL_TANACH_US_2),
    " in early 2022, almost four years ago. The editors of $UXLC received this",
    " correction from a Sefaria user, Yedidya Darshan. (At the time, the tanach.us",
    " version of $WLC was Sefaria’s default Tanakh.) This correction was submitted",
    " to the Groves Center, and appeared in $WLC 4.22. Notable digital publishers",
    " seem to take no interest in updating their close-to-$WLC texts with",
    " corrections from either $UXLC or $WLC 4.22. Their close-to-$WLC texts seem",
    " frozen. Such publishers include Oak Tree (Accordance) and Faithlife (Logos).",
]
_PARA_065 = "To summarize our answers to the questions posed at the start:"
_LIST_066 = [
    [
        "Which editions get this wrong, and why?",
        author.unordered_list(
            [
                "$BHS and most editions derived from it get this wrong.",
                [
                    "This includes $WLC prior to 4.22 and most editions derived from it, including",
                    " the $JPS HET, though the HET is heavily corrected elsewhere.",
                ],
                "$BHS got this wrong due to a transcription error.",
            ]
        ),
    ],
    [
        "Which editions get this right, and why?",
        author.unordered_list(
            [
                [
                    "All paper editions not derived from $BHS get this right. (All editions I",
                    " consulted, that is.)",
                ],
                [
                    "It is perhaps not coincidental that all the paper editions that get it right",
                    " are made in Israel, where $BHS’s influence is less strong.",
                ],
                [
                    "Some editions get this right, despite being derived from $BHS. These editions",
                    " are heavily corrected from their $BHS starting points. These editions are",
                    " $WLC 4.22, $UXLC, and editions based on $MAM.",
                ],
            ]
        ),
    ],
    [
        "Which editions got this wrong, but have been corrected?",
        author.unordered_list(
            [
                "$UXLC and $WLC got this wrong.",
                [
                    "But both have a process of user-contributed corrections that included this",
                    " correction.",
                ],
            ]
        ),
    ],
]
