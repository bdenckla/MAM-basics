from taamey_d.doc.book_codes import *
from taamey_d.doc.book_chapter_verse import *
from taamey_d.doc.html_helpers import para, unordered_list, att, implicit_maqaf
from taamey_d.doc.html_helpers import span, xheading3


def sec_body(accum, section):
    bcvi = accum, section
    return (
        para(
            "Below, I will render challenging cases in $Taamey_D &amp; three other fonts:"
        )
        + unordered_list("Taamey Frank", "$SBL_Hebrew", "$Ezra_SIL")
        + para(
            """In these challenging cases, often at least one of those three fonts struggles.
        Typically that takes the form of a collision or, if not actually a collision,
        an infelicitous crowding of marks.
        I am not showing these problems to ridicule these fonts.
        I have the utmost respect for these fine fonts &amp; their authors.
        I am showing these problems because one of the main goals of $Taamey_D
        was to avoid such collisions &amp; crowding."""
        )
        + para(
            """It is probably not coincidental that
        many of the challenging cases are not present in $UXLC.
        I suspect the corpus of concern for these fonts was limited to $UXLC or
        some other Unicode version of $WLC.
        This would make sense because, particularly in the non-Hebrew-speaking world:"""
        )
        + unordered_list(
            "$cap_UXLC not only was, but remains the only well-known Unicode Hebrew Bible.",
            """$cap_BHS not only was, but remains hugely influential.
            ($cap_UXLC used to follow $WLC, which follows $BHS closely.)""",
        )
        + _subsection_qq_with_mer_or_mun(
            _add_ssta(bcvi, "$qamats_qatan w/ $mer_dot or $mun_dot")
        )
        + _subsection_g12_tg(_add_ssta(bcvi, "$geresh-$TG &amp; $gershayim-$TG"))
        + _competing_xolam_xaser(_add_ssta(bcvi, "competing $xolam_xaser"))
        + _revia_mugrash(_add_ssta(bcvi, "$revia_mugrash"))
        + _lamed_ascender(_add_ssta(bcvi, "$lamed ascender"))
        + _dexi(_add_ssta(bcvi, "$dexi"))
        + _stress_helper_dexi(_add_ssta(bcvi, "stress-helper $dexi"))
        + _ayin_descender(_add_ssta(bcvi, "$ayin descender"))
        + _stress_helper_zarqa(_add_ssta(bcvi, "stress-helper $zarqa"))
        + _orphan_sheva(_add_ssta(bcvi, "orphan $sheva"))
        + _qupo_words(_add_ssta(bcvi, "$QUPO words"))
        + _other_dualcant_words(_add_ssta(bcvi, "other dually-cant. words"))
        + _overburdened_letters(_add_ssta(bcvi, "overburdened letters"))
    )


def _word_and_ref(word, ref):
    return span("normal-word-spacing", span("font-family-taamey-d", word) + " " + ref)


def _display_two_words(word1, ref1, word2, ref2):
    inside = _word_and_ref(word1, ref1) + " " + _word_and_ref(word2, ref2)
    return para(inside, {"class": "wide-word-spacing"})


def _divergent_versification_end(common_start, mam_end, uxlc_end):
    return (
        bcv(*common_start) + "\N{EN DASH}" + divergent_versification(mam_end, uxlc_end)
    )


def _mk_mu(mam, uxlc):
    return {"MAM": mam, "UXLC": uxlc}


def _bcv_ref_multi_decalogues(ver_exo20_mam, ver_exo20_uxlc, bcvi):
    ver_deut5_mam = ver_exo20_mam + 4
    ver_deut5_uxlc = ver_exo20_uxlc + 4
    cv_exo20_mam = "20:" + str(ver_exo20_mam)
    cv_exo20_uxlc = "20:" + str(ver_exo20_uxlc)
    cv_deut5_mam = "5:" + str(ver_deut5_mam)
    cv_deut5_uxlc = "5:" + str(ver_deut5_uxlc)
    return bcv_ref_multi(
        "/",
        (
            (BK_EXODUS, _mk_mu(cv_exo20_mam, cv_exo20_uxlc)),
            (BK_DEUTER, _mk_mu(cv_deut5_mam, cv_deut5_uxlc)),
        ),
        bcvi,
    )


def _add_ssta(in_bcvi, subsec_title_abbrev):
    accum, section = in_bcvi
    subsection = dict(section, subsec_title_abbrev=subsec_title_abbrev)
    return accum, subsection


def _subsection_qq_with_mer_or_mun(bcvi):
    return (
        """
<h3 id="h3_qq_with_mer_or_mun">The $qamats_qatan vowel with $mer9a or $munax</h3>
<p>$cap_UXLC does not use $qamats_qatan.
    In $MAM, $meteg is the only below-mark that $qamats_qatan appears with regularly.
    But, in a handful of words in $MAM, $mer9a or $munax appears with $qamats_qatan.
    Probably because these words are so rare, some fonts struggle with them.
    Below, in $Taamey_D, are two such words.
    These words are followed by the relevant pointed letters of those examples,
    rendered in all 4 of our standard fonts.
    (I will point out that the gray $maqaf below is intentional, but I will
    not elaborate on it here because it is irrelevant to the point at hand.)
</p>
"""
        + _display_two_words(
            implicit_maqaf(att("כׇּ֥ל־עַצְמוֹתַ֨י", "כׇּ֥")),
            bcv_ref(BK_PSALMS, "35:10", bcvi),
            att("עַל־כׇּל־קׇ֣דָשַׁ֔י", "קׇ֣"),
            bcv_ref(BK_EZEKIEL, "44:13", bcvi),
        )
        + """
$dis_qq_with_mer_or_mun
<p>
    Only $Ezra_SIL &amp; $Taamey_D are collision-free.
    (Actually $Ezra_SIL does have a collision, between the $munax &amp; the $qof,
    but that is unrelated to the $qamats being $qatan.)
    When Taamey Frank &amp; $SBL_Hebrew misbehave similarly,
    as they do here,
    it is not surprising, since the OpenType logic for Taamey Frank
    is derived from $SBL_Hebrew.
</p>"""
    )


def _subsection_g12_tg(bcvi):
    return (
        """
<h3 id="h3_geresh_tg_and_gershayim_tg">The $geresh-$TG &amp; $gershayim-$TG compound accents</h3>
<!-- italic-dash $geresh- -->
<!-- italic-dash gershayim- -->
<p>Five words in $MAM have, on the same letter,
$telisha_gedolah preceded by either $geresh or $gershayim.
    (Only 3 such words exist in $UXLC.)
    Some of these words, particularly those with $geresh, prove challenging to
    some fonts.
    Here are these words in our standard 4 fonts:
</p>
$dis_geresh_tg_and_gershayim_tg
<p>(References are """
        + bcv_ref(BK_SND_KINGS, "17:13", bcvi)
        + """, """
        + bcv_ref(BK_EZEKIEL, "48:10", bcvi)
        + """, """
        + bcv_ref(BK_GENESIS, "5:29", bcvi)
        + """, """
        + bcv_ref(BK_TSEFANIAH, "2:15", bcvi)
        + """, and """
        + bcv_ref(BK_LEVITICUS, "10:4", bcvi)
        + """.)
    Two of the 5 words are not stressed on the first syllable:
    $uleleh &amp; $qirvu.
    For these two words, $MAM uses a clever but novel stress-helper
    notation.
    Taamey Frank &amp; $SBL_Hebrew do not support that notation well
    on $uleleh.
</p>
<p>Note that the floating $xolam_xaser feature
    (discussed below) lessens the challenge of $zot above, because
    it lessens competition between the dot &amp; the accents.
    (All 4 fonts have this feature.)
</p>"""
    )


def _competing_xolam_xaser(bcvi):
    return (
        """
<h3 id="h3_competition_btwn_xx_and_others">Competition between $xolam_xaser &amp; other above-marks</h3>
<p>Particularly on narrow letters, $xolam_xaser &amp; other above-marks compete for space.
    $Taamey_D does its best to move the $xolam_xaser out of the way, to the left, in such cases.
    Many other fonts are not so savvy, and suffer collisions as a result.
    Note that the examples below all involve stress helpers for accents other than $pashta.
    Stress helpers for accents other than $pashta are rare in $UXLC.
    As I mentioned above,
    I am not surprised that many fonts would struggle with words not present in $UXLC,
    since I suspect that the corpus of concern for many fonts
    was limited to a Unicode version of $WLC.
    (References are """
        + bcv_ref(BK_EZEKIEL, "27:16", bcvi)
        + """, """
        + bcv_ref(BK_FST_SAMUEL, "14:24", bcvi)
        + """, and """
        + bcv_ref(BK_SND_CHRONICLES, "14:7", bcvi)
        + """.)
</p>
$dis_xolam_xaser
<p>For another example of competition between $xolam_xaser &amp; another above-mark,
    see the section below on stress-helper $zarqa.</p>"""
    )


def _revia_mugrash(bcvi):
    return (
        """
<h3 id="h3_revia_mugrash">The $revia_mugrash accent pair</h3>
<p>The $revia_mugrash accent pair is only present in the $sifrei_emet system of cantillation.
    It is composed of $revia &amp; the prepositive accent called $geresh_muqdam.
    When the first syllable is the stressed syllable, it can be challenging to
    mediate the competition for space between these two marks if they need to both
    appear above a narrow letter like $gimel.
    For example """
        + bcv_ref(BK_PSALMS, "129:2", bcvi)
        + """:</p>
$dis_revia_mugrash"""
    )


def _lamed_ascender(bcvi):
    return (
        """
<h3 id="h3_lamed_ascender">The $lamed ascender</h3>
<p>The $lamed ascender creates a variety of challenges.
    In the examples below, $Ezra_SIL struggles with the ascender.
    The other fonts do okay, though one might say that $SBL_Hebrew’s
    $gershayim comes a little too close for comfort to the ascender.
    (References are """
        + bcv_ref(BK_DANIEL, "11:24", bcvi)
        + """, """
        + bcv_ref(BK_PSALMS, "87:4", bcvi)
        + """, and """
        + bcv_ref(BK_PSALMS, "27:13", bcvi)
        + """.)
</p>
$dis_lamed_ascender
<p>Sometimes the ascender causes a problem indirectly rather than directly.
    In the word """
        + bcv_ref(BK_ISAIAH, "44:8", bcvi)
        + """ shown below, in $SBL_Hebrew &amp; $Ezra_SIL, the ascender has caused the $pashta
    to be placed far to the left, which may be fine for true (postpositive) $pashta
    but can cause problems for stress-helper $pashta.
    In this case, a stress-helper $pashta collides with a $xolam_male dot.
    Taamey Frank’s stress-helper $pashta does not collide with the $xolam_male dot,
    but it collides directly with the ascender.
</p>
$dis_lamed_ascender_indirect
<p>
    $Taamey_D avoids the problem
    by placing stress-helper $pashta roughly in the center of the $lamed,
    behind the ascender.
    This also makes ownership of the stress-helper $pashta clearer.
    Note that stress-helper $pashta is common in $UXLC,
    unlike other stress helpers, which are rare in $UXLC.
    (Aside: unlike the other three fonts, Taamey Frank does not
    place furtive $patax “early.”)
</p>"""
    )


def _dexi(bcvi):
    return (
        """
<h3 id="h3_dexi">The $dexi accent</h3>
<p>The $sifrei_emet accent $dexi can be challenging,
    particularly since it can appear
    on the same consonant as some other below-marks, most often with $meteg
    but with others such as $munax, too.
    Taamey Frank &amp; $SBL_Hebrew seem to be trying to place
    $dexi up against the vowel rather than leaving it in a prepositive position.
    This placement is not only a departure from tradition,
    but also harder to implement!
    Below are two words with $dexi, shown in $Taamey_D,
    followed by their pointed first letters shown in our standard 4 fonts of interest.
</p>
"""
        + _display_two_words(
            att("לֵֽ֭אלֹהִים", "לֵֽ֭"),
            bcv_ref(BK_PSALMS, "42:6", bcvi),
            att("שֶׁ֣֭עֹמְדִים", "שֶׁ֣֭"),
            bcv_ref(BK_PSALMS, "135:2", bcvi),
        )
        + """
$dis_dexi"""
    )


def _stress_helper_dexi(bcvi):
    return (
        """
<h3 id="h3_stress_helper_dexi">Stress-helper $dexi</h3>
<p>Because $dexi is prepositive, it does not always show which syllable is stressed.
    In $MAM, optionally, via the מ:דחי template,
    an atom with $dexi can also have a stress helper:
    a second $dexi, on the first letter of the stressed syllable.
    All fonts I’m aware of draw this stress helper
    with the same glyph as $dexi, below the letter.
    I find that confusing, since there it is easily mistaken
    for a $tarxa on the previous letter.
    A distant second problem is that a stress helper there is hard for a font
    to draw without collisions, and many fonts have such collisions,
    understandably, since they were not designed to accommodate this typographic innovation.
    (References are """
        + bcv_ref(BK_PROVERBS, "15:17", bcvi)
        + """ &amp; """
        + bcv_ref(BK_PSALMS, "25:3", bcvi)
        + """.)
</p>
$dis_stress_helper_dexi
<p>
    $Taamey_D draws every stress-helper $dexi
    as a vertical bar above the letter, which I call a top $meteg.
    Despite its name, a top $meteg is not a $meteg.
    It is just how $Taamey_D draws a stress-helper $dexi,
    and the text does not change:
    the stress helper is still a $u_dehi, like $dexi itself.
    $Taamey_D recognizes a stress helper by its position:
    it draws every $dexi that is not on the first letter of an atom
    as a top $meteg.
</p>
<p>
    $Taamey_D uses the same logic for $telisha_gedolah,
    the other prepositive accent with a stress helper:
    it draws every $telisha_gedolah that is not on the first letter of an atom
    as a stress helper centered over the letter.
    Though $pashta, $segolta, $telisha_qetana &amp; $tsinor are postpositive,
    so the logic for them is not exactly the same,
    $Taamey_D uses analogous logic for them:
    it draws every one of them that is not on the last letter of an atom
    as a stress helper centered over the letter.
</p>"""
    )


def _ayin_descender(bcvi):
    return (
        """
<h3 id="h3_ayin_descender">The $ayin descender</h3>
<p>In the word """
        + bcv_ref(BK_PSALMS, "107:12", bcvi)
        + """ below,
    you can see how, in $SBL_Hebrew, an $ayin with a descender,
    if followed by an overburdened narrow letter (here $zayin), can result in a collision.
    <!-- italic-close-paren (... $zayin) -->
    To avoid the collision, the font might use a larger advance on the $ayin
    in such contexts. Or it might include such contexts in the conditions under which
    descender-free $ayin is used.
</p>
$dis_ayin_descender_1
<p>
    Fonts are software, and as with all software, every feature added creates opportunities for new bugs to creep in.
    In the word """
        + bcv_ref(BK_PSALMS, "88:16", bcvi)
        + """ below,
    we can see that $SBL_Hebrew neglected to “tell” the descender-free $ayin glyph how
    to place $u_zarqa, and as a result it appears as a postpositive on descender-free $ayin.
    Taamey Frank, though it has only one “flavor” of $ayin, inherited the vestiges of this
    feature from $SBL_Hebrew, one of the vestiges being this bug.
</p>
$dis_ayin_descender_2
<p>
    (The different $zarqa shape in $Ezra_SIL is discussed in the next section.
    Also, the next section has more information on the confusingly-named $u_zarqa code point.)
</p>"""
    )


def _stress_helper_zarqa(bcvi):
    return (
        """
<h3 id="h3_stress_helper_zarqa">Stress-helper $zarqa</h3>
<p>The $u_zinor code point is used for true (postpositive) $zarqa
and the $sifrei_emet accent $tsinor.
    It is slightly odd that this code point is named after
    its $sifrei_emet name.
    (E.g., Unicode uses $u_tipexa not $u_hypothetical_tarxa.)
    It is also slightly odd that it is not spelled $u_hypothetical_tsinor.
    (E.g., Unicode uses $u_tsadi &amp; $u_tsere.)
    So, the name “$u_zinor” is slightly odd in a couple of ways,
    but no big deal.
</p>
<p>
    The big deal is that there is a code point named $u_zarqa
    that is not used
    (and should not be used)
    for true $zarqa.
    Its name is widely agreed to be an error.
    But due to the nature of Unicode, its name
    will not be fixed.
    The $u_zarqa code point is used for the $sifrei_emet accent $tsinnorit,
    and it can be used for stress-helper $zarqa.
    $cap_MAM &amp; $UXLC use $u_zarqa for stress-helper $zarqa.
    ($UXLC has only two such uses.)
    <!-- 2Chr 19:2 (חֲנָ֘נִי֮) &amp; 2Sam 3:8 (אָנֹ֘כִי֮). -->
    As a mnemonic, I think of $u_zarqa as
    an accidentally truncated version of $u_hypothetical_zarqahlp.
</p>
<p>
Although $MAM &amp; $UXLC use $u_zarqa for stress-helper $zarqa,
I think it would be better to use $u_zinor.
That would be analogous to what is done for other accents with
stress helpers:
they use the same code point for both the stress helper
&amp; the true accent.
Although no word in its corpus uses $u_zinor for stress-helper $zarqa,
$Taamey_D supports this.
This support is an exception to $Taamey_D’s usual policy of unconcern
for words outside its corpus.
Since version 1.1 that policy governs marks above a letter only.
Marks below a letter are placed generally.
</p>
<p>
Using $u_zarqa for stress-helper $zarqa
is like using $u_qadma for stress-helper $u_pashta,
which is not done (nor should it be done) by $MAM or $UXLC.
    (There is one word in the corpus that has both $qadma &amp; $pashta though!
    This is a dually-cantillated word in the Decalogues.
    See the section
    “<a href="#h3_qupo_words">$h3_title_qupo_words</a>”
    for information on dual cantillation.)
</p>
<p>
    In the word """
        + bcv_ref(BK_SND_SAMUEL, "3:8", bcvi)
        + """ below,
    we can see some of the challenges associated with stress-helper $zarqa.
    For each font, I show the standard $u_zarqa/$u_zinor (“zazi”)
    encoding, and then the $u_zinor/$u_zinor (“zizi”) encoding,
    which I prefer.
</p>
$dis_zizi_zazi
<p>
    Taamey Frank &amp; $SBL_Hebrew handle these two encodings differently.
    For these two fonts, the “zizi” encoding causes the accent
    to be raised up above the $xolam_xaser dot,
    a somewhat radical way of mediating
    the competition for space between those marks.
    Though somewhat radical, one might
    prefer it to the crowding seen in these two fonts
    when the “zazi” encoding is used.
    And even this crowding still requires
    a somewhat right-biased (“early”) placement for the $u_zarqa glyph.
    $Taamey_D’s glyphs for $u_zarqa &amp; $u_zinor
    are a little narrower than those of Taamey Frank &amp; $SBL_Hebrew.
    This narrower shape,
    combined with a left-biased (“late”) placement of the $xolam_xaser dot,
    makes things come
    out a little better on a narrow letter like $nun, in my opinion.
</p>
<p>
    Note that $Ezra_SIL uses a different shape
    than the other fonts for $u_zarqa &amp; $u_zinor.
    $Ezra_SIL mimics the font used in the influential $BHS edition of the $LC.
    $cap_BHS, in turn, mimics the shape used in the $LC
    for $zarqa, $tsinor, and $tsinnorit.
</p>
<p>
$cap_UXLC uses $u_zarqa for more than just
$tsinnorit &amp; stress-helper $zarqa.
It uses $u_zarqa in ten cases
where $BHS puts a $zarqa before the ascender
of a final $lamed.
$cap_BHS does this
because that’s what the $LC’s pointing scribe
did in these cases.
To me, this transcription is too literal.
But as a font author, my job is to support
every word in $UXLC regardless of such judgments.
Here’s one of the ten words:
</p>
"""
        + para(_word_and_ref("וּֽלְיִשְׁמָעֵאל֘", bcv_ref(BK_GENESIS, "17:20", bcvi)))
    )


def _orphan_sheva(bcvi):
    return (
        """
<h3 id="h3_orphan_sheva">Orphan $sheva in $yerushalayemah</h3>
<p>In words for Jerusalem,
the marks on or near the $lamed
should conform to the following pattern:</p>
<ul>
    <li>Either $patax or $qamats should appear under the $lamed.</li>
    <li>Optionally, an accent can appear either above or below the $lamed.</li>
    <li>An “orphan” vowel, $xiriq or $sheva,
        should appear in or near the space between the $lamed &amp; the next letter.
        (The next letter is always a $mem of some kind.)
    </li>
</ul>
<p>
    I call the vowel an orphan
    because its “parent” consonant, a $yod, is only implicitly present,
    because each of these words for Jerusalem is a perpetual $qere.
    If the orphan vowel is $xiriq, the word then ends with a final $mem.
    If the orphan vowel is $sheva (rare), the word then ends with a $mem and a $he,
    with a $qamats under the $mem.
    All 4 of our standard fonts place the orphan $xiriq far away from the true vowel under the $lamed.
    (The true vowel under the $lamed is $patax or $qamats.)
    In fact, with default letter spacing,
    all 4 of our standard fonts
    place the orphan $xiriq far enough the left
    to be under the final $mem.
    Below,
    I show the pointed $lamed &amp; final $mem of a Jerusalem word
    """
        + bcv_ref(BK_ISAIAH, "33:20", bcvi)
        + """
    with a $geresh accent.
    I show these letters with default letter spacing and then with wide letter spacing below.
    The wide letter spacing shows that even though in default letter spacing,
    the orphan $xiriq may appear to “belong” to the final mem,
    in fact it “belongs” to the $lamed.
</p>
$dis_LAIO_pat_ger
<p>While all 4 fonts place orphan $xiriq similarly,
    only $Taamey_D uses a position for the rare orphan $sheva
    that is analogous to orphan $xiriq, as
    in the word """
        + bcv_ref(BK_EZEKIEL, "8:3", bcvi)
        + """ below (only the suffix is shown):
</p>
$dis_LAEO_pat_ger
<p>
    The way the other 3 fonts place orphan $sheva is not wrong,
    but it is not analogous to the way they place orphan $xiriq.
    Note that if the orphan $sheva is placed too far away from the true vowel under the $lamed,
    the orphan $sheva may start to look like the $sheva-like part of a $xataf_qamats under the (non-final) $mem.
    <!-- italic-dash $sheva- -->
    I think $Taamey_D strikes a good balance between these competing goals for the orphan $sheva placement:
    notably far away from the true vowel under the $lamed, but also not too close to the $qamats under the (non-final) $mem.
</p>
<p>Above, the examples of orphan $sheva with $geresh were encoded in what I call $LAEO form:
    $lamed, “ah” vowel, $sheva, over-accent (above-accent).
    This is how $UXLC encodes such words.
    The encoding $MAM uses is $LAOcE:
    $lamed, “ah” vowel, over-accent, $u_CGJ, $sheva.
    Below we can see that some fonts do not “like” $LAOcE:
</p>
$dis_LAOcE_pat_ger
<p>
    Note that, possibly by accident, with $LAOcE, Taamey Frank looks almost the same as $Taamey_D.
    (Taamey Frank puts any marks after $u_CGJ at the left edge of the base letter,
    which is the default (zero) position for marks. In this case $lamed is the base letter.)
    The fonts that struggle with $LAOcE do not struggle with its $xiriq version, $LAOcI.
</p>
<p>
    I wonder whether many of the challenges of orphan vowels might have been alleviated
    by having a $u_hypothetical_implicit_yod code point in Unicode. Then these orphan
    vowels would only be orphans in a visual sense. In terms of their encoding, these
    vowels would have $u_hypothetical_implicit_yod as their “parent” letter.
    $u_hypothetical_implicit_yod would typically render as not only invisible but also
    taking up no space.
</p>
"""
    )


def _qupo_words(bcvi):
    return (
        to_str(xheading3("$h3_title_qupo_words", "h3_qupo_words"))
        + "\n"
        + para(
            "There are 3 sections of the Hebrew Bible"
            + " that have two systems of cantillation:"
        )
        + unordered_list(
            (bcv(BK_GENESIS, "35:22") + """ (in the Saga of Reuben)"""),
            (
                _divergent_versification_end((BK_EXODUS, "20:2"), 13, 17)
                + """ (the Exodus Decalogue)"""
            ),
            (
                _divergent_versification_end((BK_DEUTER, "5:6"), 17, 21)
                + """ (the Deuteronomy Decalogue)"""
            ),
        )
        + para(
            """
(Unfortunately, $MAM and $UXLC have different verse numbering
in the Decalogues.
Although they agree on the number of the first verse,
the number of the last verse is 4 higher in $UXLC.
Above and elsewere, we use the notation
"""
            + divergent_versification("a", "b")
            + """
to mean “verse a in $MAM and verse b in $UXLC.”)"""
        )
        + para(
            """
    In $Taamey_D’s corpus, these sections notate both systems of cantillation
    on the same set of letters.
    As a result, these sections of the Hebrew Bible are
    the sections most densely packed with typographic challenges.
    Within these challenging sections, perhaps the most challenging words are
    the two $QUPO words,
    $panay """
            + _bcv_ref_multi_decalogues(2, 3, bcvi)
            + """ &amp;
    $mitaxat """
            + _bcv_ref_multi_decalogues(3, 4, bcvi)
            + """
    These words contain letters that bear a burden of
    not only two accents but also two vowels!
    $cap_QUPO is acronym I use to describe these 4 marks:
"""
        )
        + unordered_list(
            "$qamats",
            "under-accent ($siluq or $etnaxta) ($u_meteg used for $siluq)",
            # italic-in-parens ($siluq or $etnaxta)
            # italic-close-paren (... $siluq)
            "$patax",
            "over-accent ($revia or $geresh)",
            # italic-in-parens ($revia or $geresh)
        )
        + para("Below are $panay &amp; $mitaxat in our standard 4 fonts.")
        + "$dis_QUPO_panay_QUPO_mitaxat"
        + para(
            "It is perhaps not coincidental that $SBL_Hebrew struggles with"
            + " $panay since until recently, an error in $WLC made this word"
            + " far less challenging."
            + " In other words, I suspect $panay as shown above was not part"
            + " of $SBL_Hebrew’s corpus of concern."
        )
        + para(
            "The $QUPO words vary in appearance when rendered in $Ezra_SIL,"
            " depending on what software is used."
            + " In some software, the words look great."
            + " In other software, the below-marks still look great,"
            + " but the above-accent is “late” (too far to the left)."
        )
        + para("""The $QUPO words above are shown as they appear in $MAM,
    which uses $QUcPO encoding, where the dash indicates a $u_CGJ.
    Some fonts fare better with different encodings, but I think $QUcPO
    is the best font-neutral encoding.""")
    )


def _other_dualcant_words(bcvi):
    return (
        """
<h3 id="h3_other_dualcant">Other dually-cantillated words</h3>
<p>
    Normally, dually-cantillated words mixing an above-accent &amp; a below-accent
    pose no great challenge since the two accents do not compete for space.
    But such above/below pairs can thwart other functions of the font.
    In the example """
        + _bcv_ref_multi_decalogues(12, 15, bcvi)
        + """ below, the logic to avoid collision between
    $xolam_xaser &amp; $zaqef_qatan seems to have been thwarted,
    in Taamey Frank &amp; $SBL_Hebrew.
</p>
$dis_other_dualcant
<p>
    (As an aside, note that not only is $rafeh present here, a rarity in $Taamey_D’s corpus,
    but also it is present with $dagesh. This doubly-extraordinary notation
    indicates that in one cantillation, $dagesh is present, but not in the other.
    This shows that cantillation, though primarily concerned with accents,
    can influence whether $dagesh is used, and, as we saw with the $QUPO
    words, can influence whether $patax or $qamats is used.)
</p>
<p>
    Narrow letters like $yod &amp; $vav are easily overburdened with below-marks,
    and, depending on context, may need some extra space before or after them.
    This is particularly true in the following example """
        + _bcv_ref_multi_decalogues(4, 5, bcvi)
        + """
    from the Decalogues:
</p>
$dis_overburdened_greatly"""
    )


def _overburdened_letters(bcvi):
    return (
        """
<h3 id="h3_overburdened">Overburdened letters</h3>
<p>
    Above I showed a greatly-overburdened letter, $vav, with 3 below-marks due to dual cantillation.
    But similar, albeit less extreme situations occur frequently even with the standard burden
    of a vowel &amp; a below-accent:
</p>
$dis_overburdened
<p>(References are """
        + bcv_ref(BK_SND_SAMUEL, "19:20", bcvi)
        + """, """
        + bcv_ref(BK_DEUTER, "23:14", bcvi)
        + """, and """
        + bcv_ref(BK_ISAIAH, "66:19", bcvi)
        + """.)
    Multiple below-marks are the most common cause of overburdened letters,
    but descenders can cause issues as well in some fonts.
    Below, $Ezra_SIL struggles a little, even with as wide a letter as $kaf.
    (References are """
        + bcv_ref(BK_GENESIS, "32:33", bcvi)
        + """ &amp; """
        + bcv_ref(BK_EXODUS, "27:20", bcvi)
        + """.)
</p>
$dis_descenders
"""
    )
