"""Exports gen_html_file.

Ported from the gist ``bdenckla/f04699f2a9c4eccd3220751fdb233722``, whose
``ArtScroll-Transliterated-Ashkenaz.md`` this page replaces; that gist now
holds a stub pointing here. The prose is otherwise reproduced verbatim.

That gist had a clone at ``GitRepos/Gist-ArtScroll``, and was one of the
folders ``all-repos.code-workspace`` lists until this page existed. Its clone
URL is recorded in ``in/repo_maintenance_policy.json`` under
``gitrepos_setup_rule.gists``, beside the Hebrew World gist's, which is now
the only record on this machine that the gist exists: a gist is invisible to
``gh repo list`` and its clone URL cannot be guessed from its name.

THREE HEBREW WORDS ARE REORDERED, NOT REWRITTEN. The gist has its three
rafe-bearing words -- the ones under the fourth, eleventh and twelfth
headings -- with the rafe after the sheva. (Until 2026-09-01 this paragraph
called that "Unicode-normal mark order", which fits only the dagesh-less
cluster of u-vin'cho: in the clusters of had'vorim and t'muna the gist puts
the dagesh first, an order that is neither Unicode-normal nor MAM-normal.)
MAM-basics puts the rafe among the four marks with a declared place,
before every other mark of the cluster (``mb_cmn/uni_denorm.py``, and the
first section of this repo's ``CLAUDE.md``). The two orders hold the same
characters and render identically; only the order differs. This page has all
three in MAM-normal order, and ``_hbo_checked`` below is what keeps them
there.

One link is repointed rather than reproduced: the opening paragraph's link to
the Hebrew World review, which was itself a gist and is a stub now. It goes
to the sibling page in this same directory.

The remaining changes are two, both house style rather than rewording:

* the ``$`` keys that ``dollar_sub`` requires, which carry the repo's
  single-sourced romanizations. One of those romanizations differs from the
  gist's spelling: the gist writes "sheva" where ``$shewa`` renders "shewa".
* curly double quotation marks, as every other authored page here has. The
  gist already has curly apostrophes.

The ONOCHI section's arithmetic -- one missing macron "of 18 such errors",
followed by a list of "The other 17" -- is reproduced from the gist rather
than recomputed. It checks: 1 + 4 + 1 + 1 + 1 + 1 + 3 + 1 + 1 + 2 + 1 = 17.
"""

from mb_author import author
from mb_cmn import uni_denorm


def anchor():
    return author.std_anchor(_ANCHOR, _H1_CONTENTS)


def _hbo_checked(word):
    """Hebrew lifted from the gist, guarded against a normalizing round trip.

    MAM-normal mark order puts the shin dot, the sin dot, the dagesh and the
    rafe first, in that order, and every other mark of the cluster after them.
    Unicode-normal order sorts by canonical combining class instead, which puts
    the dagesh after the vowel and the rafe after the sheva. The two orders
    render identically, so a paste through anything that normalizes is invisible
    on the page and shows up only where something compares bytes. This page's
    three rafe-bearing words are the ones at risk, and the module docstring says
    what was done with them.
    """
    assert uni_denorm.has_std_mark_order(word), word
    return author.hbo(word)


def gen_html_file(tdm_ch):
    cbody = [
        author.heading_level_1(_H1_CONTENTS),
        author.para(_PARA_INTRO_1),
        author.para(_PARA_INTRO_2),
        author.para(_PARA_INTRO_3),
        author.para(_PARA_INTRO_4),
        author.para(_PARA_INTRO_5),
        author.heading_level_2(_H2_VAIDABER),
        author.unordered_list(_LIST_VAIDABER),
        author.heading_level_2(_H2_ELOHIM),
        author.unordered_list(_LIST_ELOHIM),
        author.heading_level_2(_H2_ES),
        author.unordered_list(_LIST_ES),
        author.heading_level_2(_H2_KOL_HADVORIM),
        author.unordered_list(_LIST_KOL_HADVORIM),
        author.heading_level_2(_H2_HO_AYLE),
        author.unordered_list(_LIST_HO_AYLE),
        author.heading_level_2(_H2_LAY_MOR),
        author.unordered_list(_LIST_LAY_MOR),
        author.heading_level_2(_H2_ONOCHI),
        author.unordered_list(_LIST_ONOCHI),
        author.heading_level_2(_H2_ADONOY),
        author.unordered_list(_LIST_ADONOY),
        author.heading_level_2(_H2_ELOHECHO),
        author.unordered_list(_LIST_ELOHECHO),
        author.heading_level_2(_H2_ELLIPSIS),
        author.para(_PARA_ELLIPSIS),
        author.heading_level_2(_H2_U_VINCHO),
        author.unordered_list(_LIST_U_VINCHO),
        author.heading_level_2(_H2_TMUNA),
        author.unordered_list(_LIST_TMUNA),
        author.heading_level_2(_H2_BRAY_ACHO),
        author.para(_PARA_BRAY_ACHO),
        author.heading_level_2(_H2_KOL),
        author.para(_PARA_KOL),
        author.heading_level_2(_H2_ADONOI),
        author.para(_PARA_ADONOI),
        author.heading_level_2(_H2_CONCLUSION),
        author.para(_PARA_CONCLUSION_1),
        author.para(_PARA_CONCLUSION_2),
        author.para(_PARA_CONCLUSION_3),
        author.para(_PARA_CONCLUSION_4),
        author.para(_PARA_CONCLUSION_5),
    ]
    return author.help_gen_html_file(__file__, tdm_ch, _FNAME, _TITLE, cbody)


_TITLE = "A Review of the ArtScroll Transliterated Linear Siddur (Ashkenaz)"
_H1_CONTENTS = _TITLE
_FNAME = "review_of_artscroll_transliterated_linear_siddur.html"
_ANCHOR = author.anchor_h("document", f"./{_FNAME}")

_URL_SIDDUR = "https://www.artscroll.com/Books/9781578191512.html"
_URL_HW_REVIEW = "./review_of_hebrew_worlds_phonetic_bible.html"
_URL_MAM_WITH_DOC = "https://bdenckla.github.io/MAM-with-doc/A2-Exodus.html#c20v1"
_URL_WS_MAM = "https://he.wikisource.org/wiki/%D7%A9%D7%9E%D7%95%D7%AA_%D7%9B/%D7%98%D7%A2%D7%9E%D7%99%D7%9D"
_URL_JACOBSON = "https://bdenckla.github.io/phonetic-hbo/tnkh/A2-Exodus/20.html"
_URL_MAM = "https://purl.archive.org/mam/hebrew-wikisource"
_URL_MG = "https://mg.alhatorah.org/"
_URL_CHANTING = "https://jps.org/books/chanting-the-hebrew-bible-2/"
_URL_JACOBSON_ASHK = (
    "https://bdenckla.github.io/phonetic-hbo/tnkh-ashkenaz/A2-Exodus/20.html"
)
_URL_A_LITTLE_HEBREW = "https://www.alittlehebrew.com/transliterate/"
_URL_WS_MAM_DECALOGUE = "https://he.wikisource.org/wiki/%D7%A9%D7%9E%D7%95%D7%AA_%D7%9B/%D7%98%D7%A2%D7%9E%D7%99%D7%9D#%D7%A2%D7%A9%D7%A8%D7%AA_%D7%94%D7%93%D7%91%D7%A8%D7%95%D7%AA_%D7%91%D7%A1%D7%A4%D7%A8_%D7%A9%D7%9E%D7%95%D7%AA"

_HE_VAIDABER = _hbo_checked("וַיְדַבֵּר")
_HE_ELOHIM = _hbo_checked("אֱלֹהִים")
_HE_ES = _hbo_checked("אֵת")
_HE_ES_ASHER_YISO = _hbo_checked("אֵת אֲשֶׁר יִשָּׂא")
_HE_KOL_HADVORIM = _hbo_checked("כָּל הַדְּֿבָרִים")
_HE_KOL_DAGESHED = _hbo_checked("כָּל")
_HE_HADVORIM = _hbo_checked("הַדְּֿבָרִים")
_HE_KOL_HADEVARIM_ACCENTED = _hbo_checked("כָּל־הַדְּבָרִ֥ים")
_HE_HO_AYLE = _hbo_checked("הָאֵֽלֶּה")
_HE_LAY_MOR = _hbo_checked("לֵאמֹר")
_HE_ONOCHI = _hbo_checked("אָנֹכִי")
_HE_ADONOY = _hbo_checked("יְהֹוָה")
_HE_ELOHECHO_PHRASE = _hbo_checked("אֱלֹהֶֽיךָ אֲשֶׁר הוֹצֵאתִֽיךָ מֵאֶֽרֶץ מִצְרַֽיִם")
_HE_U_VINCHO = _hbo_checked("וּבִנְֿךָ")
_HE_TMUNA_AVOS_SIRTZACH = _hbo_checked("תְּֿמוּנָה, אָבֹת, תִרְצָח")
_HE_BRAY_ACHO = _hbo_checked("בְרֵעֲךָ")
_HE_KOL_UNDAGESHED = _hbo_checked("כָל")

_PARA_INTRO_1 = [
    "This is a review of the ArtScroll ",
    author.anchor_h(
        "Transliterated Linear Siddur - Weekday - Seif Edition", _URL_SIDDUR
    ),
    " (Ashkenaz). This review focuses on the siddur’s transliteration. This review is similar in spirit to my ",
    author.anchor_h("review of Hebrew World’s Phonetic Bible", _URL_HW_REVIEW),
    ".",
]
_PARA_INTRO_2 = "A brief summary of my review of ArtScroll’s work is as follows: this siddur provides insight into a dialect of Hebrew that may be unfamiliar to many readers, but its transliteration is somewhat inconsistent. It is hard to produce consistent transliterations without automation or a lot of proofreading labor, neither of which seems to have been deployed here."
_PARA_INTRO_3 = "We will use the siddur’s Ten Commandments (pages 290–293) as a source of examples. These are the Ten Commandments of Exodus 20 (in Parashat Yitro), not the Ten Commandments of Deuteronomy 5 (in Parashat Vaʾetḥanan). We assume that this is a reasonable sample of the rest of the siddur, but we acknowledge that this might not be true."
_PARA_INTRO_4 = [
    "ArtScroll does not number the verses of this passage. It only numbers the Commandments. Nonetheless, below I do refer to verse numbers, using a numbering that appears in many but far from all publications. To see the verse numbering I use, see any edition of $MAM using $MAM’s native verse numbering, such as ",
    author.anchor_h("$MAM with doc", _URL_MAM_WITH_DOC),
    " or ",
    author.anchor_h("Wikisource $MAM", _URL_WS_MAM),
    ". (Not all editions of $MAM use $MAM’s native verse numbering.)",
]
_PARA_INTRO_5 = "ArtScroll includes the introduction to the Ten Commandments (20:1) before it starts with the Ten Commandments proper. The first word of the intro gives us a feel for the transliteration style, and also already shows some inconsistencies."
_H2_VAIDABER = ["VAIDABER (", _HE_VAIDABER, ")"]
_LI_VAIDABER_1 = "All-caps are used for the first word of each section. (There are 11 sections: this intro is a section, and each Commandment is a section.)"
_LI_VAIDABER_2 = "Syllables are not separated."
_LI_VAIDABER_3 = "Stress is not indicated. (When stress is nonfinal, it is indicated in the accompanying pointed Hebrew, borrowing the symbol for $meteg_sl_silluq.)"
_LI_VAIDABER_4 = [
    "Cantillation does not appear on the accompanying pointed Hebrew (e.g. no $munax appears on ",
    _HE_VAIDABER,
    "). Nonetheless, from the way words are pointed (and transliterated!) later in the passage, we can see that the $taxton rather than $elyon cantillation is implied.",
]
_LI_VAIDABER_5 = "The letter “i” is used for $yod here. Presumably, this is to avoid “ay” because “ay” is dedicated to $tsere."
_LI_VAIDABER_6 = "In this word, the letter “e” rather than the pair “ay” is (accidentally?) used for $tsere. The pair “ay” is normally how $tsere is transliterated in this system. As such, I would have expected VAIDABAYR not VAIDABER. (Although “ay” for $tsere has its merits, we shall see that it causes a lot of problems, too.)"
_LI_VAIDABER_7 = [
    "Doubling (gemination) is not transliterated. We can see this because the $dagesh in the $bet of the source Hebrew word (",
    _HE_VAIDABER,
    ") is widely agreed to be a $dagesh_xazaq. E.g. a fussier (or if you prefer, more technical) transliteration might have VAIDABBER here rather than simply VAIDABER.",
]
_LIST_VAIDABER = [
    _LI_VAIDABER_1,
    _LI_VAIDABER_2,
    _LI_VAIDABER_3,
    _LI_VAIDABER_4,
    _LI_VAIDABER_5,
    _LI_VAIDABER_6,
    _LI_VAIDABER_7,
]
_H2_ELOHIM = ["Elōhim (", _HE_ELOHIM, ")"]
_LI_ELOHIM_1 = "The initial “E” is capitalized, presumably to mimic the capitalization of proper nouns in English and other Roman-alphabet languages."
_LI_ELOHIM_2 = "An “o” with a macron (ō) is used for the $xolam vowel. This is an important distinction since plain “o” is used for $qamats."
_LI_ELOHIM_3 = "Consonantal $alef is not transliterated. E.g. a fussier (or if you prefer, more technical) transliteration might have ’Elōhim or ʾElōhim here rather than simply Elōhim."
_LIST_ELOHIM = [_LI_ELOHIM_1, _LI_ELOHIM_2, _LI_ELOHIM_3]
_H2_ES = ["es (", _HE_ES, ")"]
_LI_ES_1 = "An “s” is used for $tav_rafeh, i.e. for $tav without $dagesh. This “s” for $tav_rafeh and the “o” for $qamats are the most distinctive aspects of this transliteration. Or rather, they are the most distinctive aspects of the dialect of Hebrew that this transliteration targets."
_LI_ES_2 = [
    "An “e” rather than “ay” is (accidentally?) used for $tsere, again, as in VAIDABER. Compare with “ays asher yiso” for ",
    _HE_ES_ASHER_YISO,
    " in verse 6.",
]
_LIST_ES = [_LI_ES_1, _LI_ES_2]
_H2_KOL_HADVORIM = ["kol had’vorim (", _HE_KOL_HADVORIM, ")"]
_LI_KOL_HADVORIM_1 = [
    "A distinguished $qq shape is not needed in the pointed Hebrew, since all cases of $qamats have the same sound in this dialect! (E.g. ",
    _HE_KOL_DAGESHED,
    " here.)",
]
_LI_KOL_HADVORIM_2 = [
    "Apostrophe is used for mobile $shewa, as we can see in had’vorim. The symbol for $rafeh (an above-bar) is borrowed to mark a $shewa as mobile in the pointed Hebrew, as we can see in ",
    _HE_HADVORIM,
    ".",
]
_LI_KOL_HADVORIM_3 = [
    "$Maqaf appears in neither the transliteration nor the pointed Hebrew, as we can see in “kol had’vorim” and ",
    _HE_KOL_HADVORIM,
    ", since the fully-pointed chanted word is ",
    _HE_KOL_HADEVARIM_ACCENTED,
    ".",
]
_LIST_KOL_HADVORIM = [_LI_KOL_HADVORIM_1, _LI_KOL_HADVORIM_2, _LI_KOL_HADVORIM_3]
_H2_HO_AYLE = ["ho-ayle (", _HE_HO_AYLE, ")"]
_LI_HO_AYLE_1 = [
    "The symbol for $meteg_sl_silluq is borrowed to indicate nonfinal stress in the pointed Hebrew, as we can see in ",
    _HE_HO_AYLE,
    ".",
]
_LI_HO_AYLE_2 = "A dash is used to set off a syllable starting with consonantal $alef from the preceding syllable, even though $alef itself is untransliterated. Or, if you like, non-initial consonantal $alef is transliterated as a dash."
_LIST_HO_AYLE = [_LI_HO_AYLE_1, _LI_HO_AYLE_2]
_H2_LAY_MOR = ["lay-mōr (", _HE_LAY_MOR, ")"]
_LI_LAY_MOR_1_SUBLIST = [
    "The later words shay-shes, ay-shes, and vai-kad’shay-hu seem to follow this (confusing) pattern of dash after “ay”.",
    "Words that seem to not follow this pattern include ho-ayle (already seen), and the later words hotzaysicho, achayrim, shilayshim, bayrach, and shayshes. That last one, shayshes, directly contradicts the shay-shes transliteration of a previous instance of the same pointed Hebrew word.",
]
_LI_LAY_MOR_1 = [
    "A dash separates “lay” and “mōr”, for reasons I don’t understand.",
    author.unordered_list(_LI_LAY_MOR_1_SUBLIST),
]
_LIST_LAY_MOR = [_LI_LAY_MOR_1]
_H2_ONOCHI = ["ONOCHI (", _HE_ONOCHI, ")"]
_LI_ONOCHI_1 = (
    "All-caps are used, since we are starting a section (Commandment 1) (verse 2)."
)
_LI_ONOCHI_2 = "The digraph “ch” is used for $khaf ($kaf_rafeh). It is also used for $xet, as in the later word achayrim."
_LI_ONOCHI_3_SUBLIST = [
    "This is only one of 18 such errors of a missing macron in these Ten Commandments. The other 17 are as follows: hotzaysicho, lo (4×), Elohecho, avon, avos, sh’mo, yom (3×), l’kad’sho, ta-avod, sach-mod (2×) and v’chol.",
    "I suspect this transliteration was made by hand, so it is not surprising to find many such errors.",
]
_LI_ONOCHI_3 = [
    "A macron seems missing from the “o” representing the $xolam, i.e. I would have expected ONŌCHI.",
    author.unordered_list(_LI_ONOCHI_3_SUBLIST),
]
_LIST_ONOCHI = [_LI_ONOCHI_1, _LI_ONOCHI_2, _LI_ONOCHI_3]
_H2_ADONOY = ["Adōnoy (", _HE_ADONOY, ")"]
_LI_ADONOY_1 = "Initial capital “A” is used, according to the policy we’ve already seen for proper nouns."
_LI_ADONOY_2 = "The pair “oy” is used for the $qamats_yod diphthong."
_LI_ADONOY_3 = "This is intended for a Jewish audience, so of course we see the standard euphemistic $qere (a special kind of perpetual $qere) appear in the transliteration. I mention this because I have seen many Christian-oriented transliterations that (attempt to) vocalize the tetragrammaton. Personally, I find such vocalizations a bit jarring."
_LIST_ADONOY = [_LI_ADONOY_1, _LI_ADONOY_2, _LI_ADONOY_3]
_H2_ELOHECHO = "Elōhecho asher hotzaysicho may-eretz mitzra-yim"
_LI_ELOHECHO_1 = ["Pointed Hebrew is ", _HE_ELOHECHO_PHRASE, "."]
_LI_ELOHECHO_2 = "The first four words, “Elōhecho asher hotzaysicho may-eretz”, follow patterns we have already discussed."
_LI_ELOHECHO_3_SUBLIST = [
    "We also see this later, in shoma-yim (2×), ma-yim, and va-yonach.",
    "Although “ay” for $tsere has its merits, perhaps a single letter with a diacritic would have been a better choice, such as “e” with a macron (ē). Using “ē” or similar would avoid the need to introduce dashes to solve problems that “ay” causes.",
    "On the other hand, there is merit to a transliteration like ArtScroll’s that minimizes diacritics. ArtScroll uses only a macron, and only above “o” (ō).",
]
_LI_ELOHECHO_3 = [
    "A dash is used to show the syllable boundary in what would otherwise be an ambiguous “ay” in mitzra-yim.",
    author.unordered_list(_LI_ELOHECHO_3_SUBLIST),
]
_LIST_ELOHECHO = [_LI_ELOHECHO_1, _LI_ELOHECHO_2, _LI_ELOHECHO_3]
_H2_ELLIPSIS = "[...]"
_PARA_ELLIPSIS = "I title this section with an ellipsis because at this point we’ll stop going word-for-word and just skip around to words we find notable."
_H2_U_VINCHO = ["u-vin’cho (", _HE_U_VINCHO, ") (v. 9)"]
_LI_U_VINCHO_1 = "The $shewa under the $nun is not widely agreed to be mobile, as it is here: I would have expected no apostrophe, i.e. u-vincho."
_LI_U_VINCHO_2 = "A dash follows this word’s initial $shuruq but uvitecho, the very next word, seems to defy that pattern. I find the dash in i-mecho (v. 11) similarly puzzling."
_LIST_U_VINCHO = [_LI_U_VINCHO_1, _LI_U_VINCHO_2]
_H2_TMUNA = ["t’muna, avos, sir-tzach (", _HE_TMUNA_AVOS_SIRTZACH, ")"]
_LI_TMUNA_1 = "(vv. 3, 4 & 12)"
_LI_TMUNA_2 = "Why do these cases of $qamats get “a” but all others get “o”?"
_LI_TMUNA_3 = "The word avos, in addition to its “a” being surprising (“o” expected), is also one of the 18 words missing a macron over its “o”, i.e. ovōs is expected."
_LI_TMUNA_4_SUBLIST = [
    "I.e. the dash is perhaps to make it clear that the syllables are not considered to be sirt-zach.",
    "If this is the reason for the dash before “tz”, then it is unclear why hotzaysicho was not spelled ho-tzaysicho (to distinguish from hot-zaysicho).",
]
_LI_TMUNA_4 = [
    "The dash in the word sir-tzach is perhaps to make it clear that “tz” is a digraph, not two separate letters.",
    author.unordered_list(_LI_TMUNA_4_SUBLIST),
]
_LIST_TMUNA = [_LI_TMUNA_1, _LI_TMUNA_2, _LI_TMUNA_3, _LI_TMUNA_4]
_H2_BRAY_ACHO = ["b’ray-acho (", _HE_BRAY_ACHO, ") (v. 12)"]
_PARA_BRAY_ACHO = "The “b” is surprising since the $bet has no $dagesh, i.e. it is a $vet. A “v” is expected, i.e. v’ray-acho is expected."
_H2_KOL = ["kol (", _HE_KOL_UNDAGESHED, ") (v. 9)"]
_PARA_KOL = "The “k” is surprising since the $kaf has no $dagesh, i.e. it is a $khaf. The digraph “ch” is expected, i.e. chol is expected."
_H2_ADONOI = "adōnoi (v. 10)"
_PARA_ADONOI = "The pair “oi” is surprising for the $qamats_yod diphthong. The pair “oy” is expected, i.e. adōnoy is expected."
_H2_CONCLUSION = "Conclusion"
_PARA_CONCLUSION_1 = "As I said at the start, this siddur provides insight into a dialect of Hebrew that may be unfamiliar to many readers, but its transliteration is somewhat inconsistent."
_PARA_CONCLUSION_2 = [
    "If you’re interested in seeing a different approach to transliteration of the Yitro Decalogue, targeting a different dialect of Hebrew, see my ",
    author.anchor_h("Jacobson-style transliteration", _URL_JACOBSON),
    " of the Al-Hatorah edition of ",
    author.anchor_h("$MAM", _URL_MAM),
    ". (That edition of $MAM forms the core of the ",
    author.anchor_h("Al-Hatorah Mikraot Gedolot", _URL_MG),
    "). (By “Jacobson-style”, I mean the style laid out in ",
    author.anchor_h(
        "Chanting the Hebrew Bible, Second Edition: The Art of Cantillation",
        _URL_CHANTING,
    ),
    ".)",
]
_PARA_CONCLUSION_3 = [
    "Here is an ",
    author.anchor_h("Ashkenazic Jacobson-style transliteration", _URL_JACOBSON_ASHK),
    " of the Yitro Decalogue, which is perhaps more relevant in this context.",
]
_PARA_CONCLUSION_4 = [
    "If you’d like to experiment with an interactive ArtScroll-emulating transliterator, try the ArtScroll setting of ",
    author.anchor_h("the transliterator at “A Little Hebrew”", _URL_A_LITTLE_HEBREW),
    ".",
]
_PARA_CONCLUSION_5 = [
    "If you’d like to see the pointed Hebrew for the $taxton cantillation of the Yitro Decalogue, see the one on ",
    author.anchor_h("Wikisource $MAM", _URL_WS_MAM_DECALOGUE),
    ".",
]
