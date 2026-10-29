from taamey_d.doc import misc_helpers
from taamey_d.doc.book_codes import *
from taamey_d.doc.book_chapter_verse import *
from taamey_d.doc.html_helpers import *


def sec_body(accum, section):
    bcvi = accum, section
    return (
        para("""This section describes the most distinctive features of
        $Taamey_D, as compared to Taamey Frank.""")
        + _unicode_18_mudgash_points()
        + _upside_down_qq(_add_ssta(bcvi, "upside-down $qamats_qatan"))
        + _xataf_qq(_add_ssta(bcvi, "$xataf_qamats_qatan"))
        + _short_meteg(_add_ssta(bcvi, "short $meteg"))
        + _ax_and_yby(_add_ssta(bcvi, "$atnax_hafu9 &amp; $yerax_ben_yomo"))
        + ""
    )


def _unicode_18_mudgash_points():
    mam_atom = "לׅׄוּׅׄלֵׅ֗ׄאׅׄ"
    return (
        to_str(
            xheading3(
                "Unicode 18 $sheva_na and $dagesh_xazaq",
                "h3_unicode_18_mudgash_points",
            )
        )
        + para(
            "The Unicode 18 Hebrew code chart assigns U+05C8 "
            "$unicode_name_sheva_na_mudgash and U+05C9 "
            "$unicode_name_dagesh_xazaq_mudgash. "
            "$Taamey_D supports U+05C8 and U+05C9."
        )
        + para(
            "During a transition that may last months or years, text-entry and "
            "text-processing software may not yet let users enter, preserve, or "
            "pass through the new code points even when the selected font supports "
            "them. $Taamey_D therefore also provides a <code>lodot</code> mode of "
            "access: ordinary $sheva followed by U+05C5 "
            "$unicode_name_lower_dot selects $sheva_na, and ordinary $dagesh "
            "followed by U+05C5 selects $dagesh_xazaq. This mode is a transitional "
            "hack, not an alternate permanent encoding. New text should use U+05C8 "
            "and U+05C9 whenever the complete software path supports them."
        )
        + _unicode_18_access_table()
        + para("In the examples, bet merely anchors the combining marks.")
        + para(
            "The <code>lodot</code> hack collides with the plain meaning of one "
            "$MAM atom, the word "
            + '<span dir="rtl" class="font-family-taamey-d">'
            + att(mam_atom, "וּׅ")
            + "</span> at "
            + bcv(BK_PSALMS, "27:13")
            + ". The vav has U+05BC $unicode_name_dagesh_or_mapiq followed by "
            "U+05C5 $unicode_name_lower_dot. On that vav before $lamed, "
            "$Taamey_D preserves the lower dot rather than interpreting the "
            "sequence as $dagesh_xazaq. This is a hack undoing a hack."
        )
        + para(
            "No atom is expected ever to need $sheva followed by lower dot with "
            "its plain meaning, so $Taamey_D has no deliberate hack that restores "
            "a literal lower dot after $sheva. Except on final kaf, "
            "<code>lodot</code> mode always interprets $sheva followed by lower "
            "dot as $sheva_na. Final kaf never needs $sheva_na; $Taamey_D forms "
            "its special final-kaf $sheva glyph before <code>lodot</code> "
            "processing, so <code>lodot</code> access to $sheva_na is unavailable "
            "on final kaf."
        )
    )


def _unicode_18_access_table():
    example_attrs = {"dir": "rtl", "class": "font-family-taamey-d"}
    rows = (
        xtable_row(
            (
                xtable_data_cell("$sheva_na"),
                xtable_data_cell(xcode("U+05C8")),
                xtable_data_cell("ב׈", example_attrs),
                xtable_data_cell(xcode("U+05B0 U+05C5")),
                xtable_data_cell("בְׅ", example_attrs),
            )
        ),
        xtable_row(
            (
                xtable_data_cell("$dagesh_xazaq"),
                xtable_data_cell(xcode("U+05C9")),
                xtable_data_cell("ב׉", example_attrs),
                xtable_data_cell(xcode("U+05BC U+05C5")),
                xtable_data_cell("בּׅ", example_attrs),
            )
        ),
    )
    inside = tuple(("\n    ", row) for row in rows)
    return to_str(
        xtable(
            (
                "Point",
                '<abbr title="Unicode 18 sequence">U18 seq.</abbr>',
                '<abbr title="Unicode 18 example">U18 ex.</abbr>',
                '<abbr title="lodot sequence"><code>lodot</code> seq.</abbr>',
                '<abbr title="lodot example"><code>lodot</code> ex.</abbr>',
            ),
            sum(inside, tuple()),
        )
    )


def _upside_down_qq(bcvi):
    return (
        to_str(xheading3("Upside-down $qamats_qatan", "h3_upside_down_qq"))
        + para(
            """
    As in many fonts, in $Taamey_D
    it can be hard to distinguish $qamats_qatan from normal $qamats.
    (Despite what its name might suggest, $qamats_qatan is slightly taller.)
    $Taamey_D provides a stylistic set, <code>ss03</code>, in which the
    $qamats_qatan shape is upside-down.
    This makes it easy to distinguish.
    Here is a word """
            + bcv_ref(BK_GENESIS, "6:15", bcvi)
            + """
    rendered both ways:
"""
        )
        + to_str(_QAMATS_QATAN_HAFUKH_TABLE)
        + para("""
(This word is from $MAM since $UXLC does not use $qamats_qatan.)
This upside-down feature is mainly intended for use within
this document, but it might find use in other places such as teaching
materials.
""")
    )


def _xataf_qq(bcvi):
    return (
        to_str(xheading3("The $xataf_qamats_qatan vowel", "h3_xqq"))
        + """<p>
    $Taamey_D provides a stylistic set, <code>ss01</code>, in which the
    glyph for $xataf_qamats matches $qamats_qatan.
    Below I render an example word """
        + bcv_ref("Isaiah", "66:12", bcvi)
        + """
    in default $Taamey_D, and
    in $Taamey_D with <code>ss01</code> selected.
    Corresponding upside-down versions are provided as well.
    This word’s third $qamats is a normal $qamats,
    which helps as a reference.
    Letters with matching $qamats shapes are highlighted.
</p>
"""
        + to_str(_XATAF_QAMATS_QATAN_TABLE)
    )


def _short_meteg(bcvi):
    return (
        """
<h3>The $qamats_qatan vowel with a short $meteg</h3>
<p>$MAM records two “$qamats variants” of some words.
    <!-- italic-opening-double-quotation-mark “$qamats ...” -->
    These are words having a $qamats that is:
    <ul>
        <li>a $qamats_qatan, according to theory
        (abbrev. ד (<span class="hair-space-after">$dalet</span>))</li>
        <!-- italic-in-parens ($dalet) -->
        <li>a normal $qamats, according to Sephardic practice
        (abbrev. ס ($same9))</li>
        <!-- italic-in-parens ($same9) -->
    </ul>
    <p>
    For example, below are $MAM’s two variant pointings of a word """
        + bcv_ref(BK_GENESIS, "19:34", bcvi)
        + "."
        + """
    The pointings are rendered in both default and upside-down $Taamey_D.
    The $mem whose $qamats varies is highlighted.
    Below I am just showing the “$qamats variants” feature of $MAM:
    <!-- italic-opening-double-quotation-mark “$qamats ...” -->
    I am not showing the short $meteg feature of $Taamey_D yet.
</p>
"""
        + to_str(_QQ_VARIANT_TABLE)
        + """
<p>
    $Taamey_D provides a stylistic set, <code>ss02</code>, in which the
    glyph for $qamats_qatan has a short $meteg.
    This allows both variants to be presented on a single word.
    A $qamats_qatan with a small $meteg
    represents a $qamats that is $qatan only in the theoretical variant.
    Below is our example theoretical variant shown
    with <code>ss02</code> selected
    (in addition to <code>ss01</code>, for $xataf_qamats_qatan):
</p>
"""
        + to_str(_METEG_QATAN_TABLE)
    )


def _ax_and_yby(bcvi):
    return (
        to_str(
            xheading3(
                "Distinct $atnax_hafu9 &amp; $yerax_ben_yomo", "h3_distinct_ah_and_yby"
            )
        )
        + para(
            "This phrase "
            + bcv_ref(BK_PSALMS, "5:10", bcvi)
            + " shows that $Taamey_D distinguishes"
            + " $yerax_ben_yomo from $atnax_hafu9:"
        )
        + """<p>
    <span class="font-family-taamey-d">
        כִּ֤י
        """
        + att("אֵ֪ין", "אֵ֪")
        + """
        בְּפִ֡יהוּ
        נְכוֹנָה֮
        """
        + att("קִרְבָּ֢ם", "בָּ֢")
        + """
        הַ֫וּ֥וֹת
    </span>
</p>
<p>Taamey Frank &amp; many other fonts do not distinguish these accents.
    Such fonts give an $atnax_hafu9 shape for both code points.
    This shortcoming likely stems from the influence of $BHS.
</p><p>
$cap_BHS is so influential that even its shortcomings
still reverberate through the Biblical world, showing up not only
in other editions of the Hebrew Bible but also in fonts!
$cap_BHS identifies an accent which it calls
“$Galgal_vel_Jerax” (“$galgal or $yerax [$ben_yomo]”).
<!-- italic-in-double-quotation-marks “$Galgal_vel_Jerax” -->
<!-- italic-opening-double-quotation-mark “$galgal ...” -->
<!-- italic-in-square-brackets [$ben_yomo] -->
So far so good, since $yerax_ben_yomo is also known as $galgal.
But then things fall short in the following ways:
</p>
"""
        + _GALGAL_LIST_1
        + para("So, many fonts did the following:")
        + _GALGAL_LIST_2
        + para(
            """$cap_UXLC used to follow $WLC, which follows $BHS closely.
    So, $UXLC used to use only the $yerax_ben_yomo code point.
    $cap_UXLC started to distinguish $yerax_ben_yomo from $atnax_hafu9
    in version 1.3, released on 19 October 2021.
    To be able to see this distinction, """
            + anchor("https://tanach.us", "tanach.us")
            + """ ($UXLC’s canonical edition) switched its default font
    to $Taamey_D.
    Formerly it used $SBL_Hebrew which, like many fonts, prevents
    this distinction from being seen,
    forcing even editions that make this distinction to still
    look like $BHS!"""
        )
    )


def _add_ssta(in_bcvi, subsec_title_abbrev):
    accum, section = in_bcvi
    subsection = dict(section, subsec_title_abbrev=subsec_title_abbrev)
    return accum, subsection


_QG = span("hair-space-before hair-space-after", "$qamats_gadol")
#
_QQH_EXAMPLE_1 = "רׇחְבָּ֔הּ"
_QAMATS_QATAN_HAFUKH_TABLE_CLASSES = (
    # TODO: use <th> not <td> for labels, perhaps with scope="row"
    ("font-family-taamey-d", ""),
    ("font-family-taamey-d qamats_qatan_hafukh", ""),
)
_QAMATS_QATAN_HAFUKH_TABLE = misc_helpers.en_by_two_table(
    ("", ""),  # no header
    ((_QQH_EXAMPLE_1, "$Taamey_D"), (_QQH_EXAMPLE_1, ("$Taamey_D ", xcode("ss03")))),
    _QAMATS_QATAN_HAFUKH_TABLE_CLASSES,
    row_tad=False,
)
#
_XQQ_EXAMPLE_1 = "תְּשׇׁעֳשָֽׁעוּ׃"
_XATAF_QAMATS_QATAN_TABLE_CLASSES = (
    ("", " xataf_qamats_qatan"),
    (" qamats_qatan_hafukh", " xataf_qamats_qatan_hafukh"),
)
_XATAF_QAMATS_QATAN_TABLE = misc_helpers.en_by_two_table(
    ("$Taamey_D", ("$Taamey_D ", xcode("ss01"))),
    misc_helpers.two((att(_XQQ_EXAMPLE_1, "עֳשָֽׁ"), att(_XQQ_EXAMPLE_1, "שׇׁעֳ"))),
    _XATAF_QAMATS_QATAN_TABLE_CLASSES,
)
#
_QQ_VARIANT_TABLE_CLASSES = (
    ("xataf_qamats_qatan", "xataf_qamats_qatan"),
    ("xataf_qamats_qatan_hafukh", " xataf_qamats_qatan_hafukh"),
)
_QQ_VARIANT_TABLE = misc_helpers.en_by_two_table(
    ("ד", "ס"),
    misc_helpers.two((att("מִֽמׇּחֳרָ֔ת", "מׇּ"), att("מִֽמָּחֳרָ֔ת", "מָּ"))),
    _QQ_VARIANT_TABLE_CLASSES,
)
#
_METEG_QATAN_TABLE_CLASSES = (
    ("qamats_qatan_meteg_qatan",),
    ("qamats_qatan_meteg_qatan_hafukh",),
)
_METEG_QATAN_TABLE = misc_helpers.en_by_two_table(
    ("ד+ס",),
    misc_helpers.two_by_two(att("מִֽמׇּחֳרָ֔ת", "מׇּ")),
    _METEG_QATAN_TABLE_CLASSES,
)
#
_GALGAL_LIST_1 = unordered_list(
    "$cap_BHS gives an $atnax_hafu9 shape to “$Galgal_vel_Jerax.”",
    # <!-- italic-in-double-quotation-marks “$Galgal_vel_Jerax” -->
    "$cap_BHS does not identify a distinct $atnax_hafu9 accent.",
)
_GALGAL_LIST_2 = unordered_list(
    "Following $BHS, they gave an $atnax_hafu9 shape to $yerax_ben_yomo.",
    "Quite reasonably, they gave an $atnax_hafu9 shape to $atnax_hafu9.",
)
