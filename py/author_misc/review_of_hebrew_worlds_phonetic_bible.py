"""Exports gen_html_file.

Ported from the gist ``bdenckla/7e578526559cbbfc2d54a1bc0c827072``, whose
``main.md`` this page replaces; that gist now holds a stub pointing here. The
prose is otherwise reproduced verbatim.

That gist had a clone at ``GitRepos/Gist-Hebrew-World``, removed on 2026-08-31
(Ben's decision) once this page existed. Its clone URL is recorded in
``in/repo_maintenance_policy.json`` under ``gitrepos_setup_rule.gists``, which
is now the only record on this machine that the gist exists -- a gist is
invisible to ``gh repo list`` and its clone URL cannot be guessed from its name.

One accent name is corrected rather than reproduced (Ben's decision,
2026-08-31). The second bullet under the fourth chanted word gives the source
word כׇּל־הַדְּבָרִ֥ים "with its accent", and the gist names that accent
tipḥa. Exodus 20:1 in ``in/mam-ws/A2-Exodus.json`` has merkha there; tipeḥa is
the accent of the next chanted word, הָאֵ֖לֶּה. So this page says merkha, and
the gist's revision history keeps what it said before.

The remaining changes are three, all house style rather than rewording:

* the ``$`` keys that ``dollar_sub`` requires, which carry the repo's
  single-sourced romanizations. One of those romanizations differs from the
  gist's spelling: the gist writes "sheva" where ``$shewa`` renders "shewa".
* curly quotation marks and apostrophes, as every other authored page here has.
* the eleven screenshots, which the gist hotlinked from GitHub's gist asset
  CDN and which now live in ``MAM-with-doc/gh-pages/misc/img/hebrew_world/``.
"""

from mb_author import author
from mb_cmn import uni_denorm
from mb_misc import mb_html

_IMG_DIR = "hebrew_world"


def anchor():
    return author.std_anchor(_ANCHOR, _H1_CONTENTS)


def _hbo_checked(word):
    """Hebrew lifted from the gist, guarded against a normalizing round trip.

    MAM-normal mark order puts the dagesh before the vowel and Unicode-normal
    order puts it after. The two render identically, so a paste through
    anything that normalizes is invisible on the page and shows up only where
    something compares bytes. Three of this page's four Hebrew words arrived in
    Unicode order exactly that way on 2026-08-31, and were restored from the
    gist's own bytes. This assertion is what makes a repeat loud.
    """
    assert uni_denorm.has_std_mark_order(word), word
    return author.hbo(word)


def _img(fname, width_em):
    return author.para_for_img(f"{_IMG_DIR}/{fname}", width_em=width_em)


def gen_html_file(tdm_ch):
    cbody = [
        author.heading_level_1(_H1_CONTENTS),
        author.para(_PARA_INTRO),
        author.para(_PARA_FIRST_WORD),
        _img("Exod 20v1 וידבר -- Hebrew World.png", 15.2),
        author.unordered_list(_LIST_FIRST_WORD),
        author.para(_PARA_NEXT_WORD),
        _img("Exod 20v1 אלהים -- Hebrew World.png", 8.1),
        author.unordered_list(_LIST_DIVINE_NAMES),
        author.para(_PARA_CATERS),
        author.para(_PARA_ACUTE),
        author.para(_PARA_DOUBLED_LETTERS),
        _img("Exod 20v11 השביעי -- Hebrew World.png", 11.8),
        author.para(_PARA_VERSE_ELEVEN),
        author.para(_PARA_RETURNING),
        author.para(_PARA_FOURTH_WORD),
        _img("Exod 20v1 כל־הדברים -- Hebrew World.png", 19.9),
        author.para(_PARA_FOURTH_IS_COMPOUND),
        author.unordered_list(_LIST_FOURTH_WORD),
        author.para(_PARA_LOW_MAQAF),
        _img("Exod 20v1 כל־הדברים low maqaf -- Hebrew World.png", 11.0),
        author.para(_PARA_FIFTH_WORD),
        _img("Exod 20v1 האלה -- Hebrew World.png", 8.4),
        author.para(_PARA_VERSE_TWO),
        _img("Exod 20v2 אנכי -- Hebrew World.png", 9.2),
        author.para(_PARA_ALEF_AYIN),
        _img("Exod 20v6 לאלפים -- Hebrew World.png", 11.0),
        author.para(_PARA_AND_VERSE_NINE),
        _img("Exod 20v9 ועשית -- Hebrew World.png", 10.2),
        author.para(_PARA_XATAF_PATAX),
        author.para(_PARA_VERSE_THREE),
        _img("Exod 20v3 לא־יהיה -- Hebrew World.png", 13.1),
        author.para(_PARA_SURPRISED),
        author.para(_PARA_VERSE_SEVEN),
        _img("Exod 20v7 את־שמו -- Hebrew World.png", 10.3),
        author.para(_PARA_APOSTROPHE),
        author.para(_PARA_REVERSE_ENGINEER),
        author.para(_PARA_MULTIPLE_NOTATIONS),
        author.para(_PARA_SAFFA),
    ]
    return author.help_gen_html_file(__file__, tdm_ch, _FNAME, _TITLE, cbody)


_TITLE = "A Review of Hebrew World’s Phonetic Bible"
_H1_CONTENTS = _TITLE
_FNAME = "review_of_hebrew_worlds_phonetic_bible.html"
_ANCHOR = author.anchor_h("document", f"./{_FNAME}")

_URL_PHONETIC_BIBLE = "https://www.hebrewworld.com/Phonetic-Bible.html"
_URL_SAFFA = "http://hebrewworks.com/Transliteration.htm"

_ANC_PHONETIC_BIBLE = author.anchor_h(
    "Hebrew/English Phonetic Bible", _URL_PHONETIC_BIBLE
)
_ANC_SAFFA = author.anchor_h("Saffa", _URL_SAFFA)

_HE_VAYEDABER = _hbo_checked("וַיְדַבֵּ֣ר")
_HE_KOL_HADEVARIM = _hbo_checked("כׇּל־הַדְּבָרִ֥ים")
_HE_KOL = _hbo_checked("כׇּל")
_HE_LO_YIHYE = _hbo_checked("לֹֽא־יִהְיֶ֥ה")

_PARA_INTRO = [
    ["This is a review of Hebrew World’s digital product called the "],
    [_ANC_PHONETIC_BIBLE],
    [". We will use Exodus 20 as a source of examples."],
]
_PARA_FIRST_WORD = """Taking a look at the first word of the chapter gives us a
feel for the transliteration style:""".replace("\n", " ")

_LI_CAPITAL_V = """The V is capitalized because they use English-like
capitalization. In their scheme, each verse is likened to a sentence. (Not shown
here is that, correspondingly, a period appears at the end of each verse.) This
equation of verse and sentence is limited to their phonetic transliteration; the
English translation they provide has its own, independent punctuation, including
its own sentence divisions.""".replace("\n", " ")
_LI_MID_DOT = """The syllables are separated by a fairly heavy mid-dot (aka
interpunct).""".replace("\n", " ")
_LI_DAGESH = [
    ["The $dagesh in the $bet of the source Hebrew word ("],
    [_HE_VAYEDABER],
    [
        ") is I think widely agreed to be a $dagesh_xazaq,"
        " so we can see that they do not make any distinctions related to"
        " gemination (doubling). E.g. a fussier (or if you prefer, more"
        " technical) transliteration might have Va·ye·dab·ber here rather than"
        " simply Va·ye·da·ber."
    ],
]
_LI_TROPE_MARKS = [
    ["Above I have given the source Hebrew word ("],
    [_HE_VAYEDABER],
    [
        ") with its trope mark, $munax, but this and all other words in"
        " Hebrew World’s Phonetic Bible appear without any trope marks or"
        " $gaya_with_half_ring_for_ayin marks. The only marks related to the"
        " trope system that appear are $maqaf and $sof_pasuq (if indeed you"
        " consider these marks to be related to the trope system)."
    ],
]
_LI_NO_STRESS = """No indication of stress is given since the stress in this word
is final and final stress is, sensibly enough, treated as the default stress in
this transliteration scheme.""".replace("\n", " ")
_LI_SHEWA_AS_TSERE = """We can see from this word that vocal $shewa is treated
the same as $tsere, namely, with an “e”. (And, from other words, we can see that
$segol and $xataf_segol map to “e” as well.)""".replace("\n", " ")
_LI_SHEWA_VOCAL = """Perhaps more interesting than its representation as “e” is
the fact that the $shewa on the $yod is considered vocal at all. I.e. some would
consider that $shewa to be resting rather than vocal, which would result in a
transliteration such as Vay·da·ber.""".replace("\n", " ")
_LIST_FIRST_WORD = [
    _LI_CAPITAL_V,
    _LI_MID_DOT,
    _LI_DAGESH,
    _LI_TROPE_MARKS,
    _LI_NO_STRESS,
    _LI_SHEWA_AS_TSERE,
    _LI_SHEWA_VOCAL,
]

_PARA_NEXT_WORD = "Let’s move on to the next word:"
_LIST_DIVINE_NAMES_INNER = [
    "are not syllable-divided",
    "are stress-marked even though the stress is final (acute accent on “i”)",
    "are capitalized (presumably because in English terms, they are proper nouns)",
]
_LI_DIVINE_NAMES = [
    "Divine names, in this scheme:",
    author.unordered_list(_LIST_DIVINE_NAMES_INNER),
]
_LI_ALEF_NOT_TRANSCRIBED = """Here we see that $alef is not transcribed. E.g. a
fussier (or if you prefer, more technical) transliteration might have ’Elohím or
ʾElohím here rather than simply Elohím.""".replace("\n", " ")
_LIST_DIVINE_NAMES = [_LI_DIVINE_NAMES, _LI_ALEF_NOT_TRANSCRIBED]

_PARA_CATERS = """We can see that this scheme caters to the English speaker not
only narrowly, in its choice of letters and letter-pairs, but also more broadly,
in its choice to use capitalization and punctuation (period) in a manner
analogous to their use in English.""".replace("\n", " ")
_PARA_ACUTE = """Note that the use of an acute accent on the vowel of the
stressed syllable, though having no analogy in English, may be familiar to
English speakers if they have even briefly studied a Latin language that uses a
similar system, such as Spanish.""".replace("\n", " ")
_PARA_DOUBLED_LETTERS = """This stress-marking system becomes somewhat awkward
for vowel sounds represented by doubled letters such as “ee”, as in verse
11:""".replace("\n", " ")
_PARA_VERSE_ELEVEN = """(Their verse 11 is verse 10 in some editions. Their text,
both in the location of its verse numbers and its $sof_pasuq marks, reflects a
version of the $taxton cantillation not present in the Tiberian manuscripts. It
is a version of the $taxton that, while centuries old, and thus “traditional,” is
nonetheless part of the printed tradition rather than the manuscript
tradition.)""".replace("\n", " ")
_PARA_RETURNING = """Returning from that digression to the topic of
stress-marking, note that with Elohím we have seen that they avoid the
awkwardness that would be present in Elohéem. But they appear to use single-i and
double-e (i and ee) interchangeably, i.e. inconsistently. A similar
interchangeable inconsistency appears to exist with single-u and double-o (u and
oo), but at least this is documented in their introduction.""".replace("\n", " ")
# The source italicizes "et", the transliteration of אֵת. It gets the
# "romanized" class directly rather than a "$et" key of its own, because that
# key's undollared form would fire _check_no_undollared on the "et" of
# "et-sh’mo" further down this same page.
_ROM_ET = mb_html.span_c("et", "romanized")
_PARA_FOURTH_WORD = [
    ["Let’s skip the third word ("],
    [_ROM_ET],
    [") and move on to the fourth:"],
]
_PARA_FOURTH_IS_COMPOUND = [
    ["(This $maqaf compound is the fourth "],
    [author.emphasis("chanted")],
    [" word; by another definition of “word” it includes both the fourth and"],
    [" fifth words.)"],
]

_LI_DASH_FOR_MAQAF = """A dash (with generous side-bearings) is used where $maqaf
appears in the source. Perhaps this is phonetically relevant, suggesting
something different (more?) than a syllable break. But perhaps it is only
semantically relevant to preserve this type of source punctuation.""".replace("\n", " ")
_LI_SHEWA_ON_DALET = [
    ["Here we see another $shewa (on $dalet) interpreted as vocal (the source"],
    [" word is "],
    [_HE_KOL_HADEVARIM],
    ["), but I think this one is less contentious than the one we saw in "],
    [_HE_VAYEDABER],
    [". (Here I give the source word ("],
    [_HE_KOL_HADEVARIM],
    [") not only with its accent ($merkha) but also using Unicode $qq in "],
    [_HE_KOL],
    [". Hebrew World’s product makes no $qamats distinctions.)"],
]
_LIST_FOURTH_WORD = [_LI_DASH_FOR_MAQAF, _LI_SHEWA_ON_DALET]

_PARA_LOW_MAQAF = """A minor point (but one I still find worth noting) is that
Hebrew World’s $maqaf is oddly low: it looks more like an English dash than a
traditional (high) $maqaf:""".replace("\n", " ")
_PARA_FIFTH_WORD = """The fifth word gives us an example of non-final (and
therefore explicit) stress:""".replace("\n", " ")
_PARA_VERSE_TWO = "The first word of verse 2 is as follows:"
_PARA_ALEF_AYIN = """Here we see the tendency of this product to not separate
$alef or $ayin syllables. I find this odd. It is one thing to give neither $alef
nor $ayin any mark of its own; this is a margin on which many transliteration
schemes differ. But treating syllables starting with $alef or $ayin as
non-syllables seems to deny phonetic reality. This phenomenon (bug?) is not
confined to initial $alef and $ayin. E.g. in verse 6:""".replace("\n", " ")
_PARA_AND_VERSE_NINE = "and in verse 9:"
_PARA_XATAF_PATAX = """(In the verse 6 example above, the first ‘a’ in the ‘ala’
of la·ala·fim is merely a $xataf_patax, which could justify attaching it to the
‘la’ syllable rather than considering it to be a syllable of its own. But that
would be inconsistent with the treatment of all other $xataf vowels in this
transliteration.)""".replace("\n", " ")
_PARA_VERSE_THREE = [
    ["The first (chanted) word of (Hebrew World’s) verse 3 has what was to me a"],
    [" surprising transcription of "],
    [_HE_LO_YIHYE],
    [":"],
]
_PARA_SURPRISED = """I was surprised to find not only the $shewa to be vocal but
also given an “i” rather than “e” vowel-value. But just because I was surprised
doesn’t mean this is wrong. It may just represent a tradition that I am unaware
of.""".replace("\n", " ")
_PARA_VERSE_SEVEN = """For now at least, we will conclude our review with what
seems to be an interchangeably inconsistent use of apostrophe and “e” for vocal
$shewa in verse 7:""".replace("\n", " ")
_PARA_APOSTROPHE = """(Reasonably enough, this apostrophe seems to function not
only as an ultra-short vowel but also as a syllable divider. I.e. et-sh’·mo could
be considered a little awkward-looking.)""".replace("\n", " ")
_PARA_REVERSE_ENGINEER = """It is possible that what I have identified as
inconsistencies are just consistencies whose rules I have not been able to
“reverse engineer”. In that case, they are just failures in documentation. Or
perhaps the inconsistencies do not follow rules, but are still intentional (not
viewed as bugs). I assume this is the case with the documented interchangeability
of u and oo. They are documented as representing the same sound, but no rule is
given for why “u” might be used in one case and “oo” in another case.""".replace(
    "\n", " "
)
_PARA_MULTIPLE_NOTATIONS = """Even if all interchangeabilities were documented,
the wisdom of introducing multiple notations for the same sound might reasonably
be questioned, as presumably the existence of multiple notations for the same
sound in the source (pointed Hebrew) is one of the reasons for a phonetic
transcription in the first place!""".replace("\n", " ")
_PARA_SAFFA = [
    ["The inconsistencies that seem to characterize this transliteration are"],
    [" particularly surprising from a company that also offers automatic (and"],
    [" therefore presumably consistent?) transliteration software (part of its "],
    ["“"],
    [_ANC_SAFFA],
    ["” product)."],
]
