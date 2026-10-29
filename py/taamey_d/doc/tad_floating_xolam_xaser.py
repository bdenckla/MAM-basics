from taamey_d.doc import misc_helpers
from taamey_d.doc.html_helpers import unordered_list, para
from taamey_d.doc.book_codes import *
from taamey_d.doc.book_chapter_verse import *
from taamey_d.doc.html_helpers import to_str, att


def sec_body(accum, section):
    bcvi = accum, section
    return (
        para("""In $Taamey_D, a $xolam_xaser dot sometimes floats forward onto
            the right arm of an $alef, as in the words
            below:""")
        + to_str(_alef_xolam_table_2(bcvi))
        + para("""(The affected syllables are highlighted and repeated with wide
            letter spacing.)""")
        + para("""This float only happens when the $alef is playing
            a vowel role, i.e. when the $alef is a mater lectionis.
            When the $alef is playing a consonant role,
            the $xolam_xaser dot does not float forward, as in
            the words below:""")
        + to_str(_alef_xolam_table_1(bcvi))
        + para("""(The syllables starting with $alef are highlighted.
            Those syllables and their preceding letters are
            repeated with wide letter spacing.)""")
        + para("""$Taamey_D behaves like this in order to match the behavior of
            Taamey Frank, which likely inherited this behavior from
            $SBL_Hebrew. $SBL_Hebrew and $Ezra_SIL likely have this behavior
            in order to mimic $BHS.""")
        + ""
    )


def _alef_xolam_table_1(bcvi):
    table_classes = (("",) * 4, ("wide-letter-spacing",) * 4)
    table = misc_helpers.en_by_two_table(
        (
            "$yavo7u " + bcv_ref(BK_GENESIS, "6:4", bcvi),
            "$bevo7o " + bcv_ref(BK_EZEKIEL, "26:10", bcvi),
            "$lero7ey " + bcv_ref(BK_KOHELET, "7:11", bcvi),
            "$umlo7ah " + bcv_ref(BK_PSALMS, "89:12", bcvi),
        ),
        (
            (
                att("יָבֹ֜אוּ", "אוּ"),
                att("בְּבֹאוֹ֙", "אוֹ֙"),
                att("לְרֹאֵ֥י", "אֵ֥י"),
                att("וּ֝מְלֹאָ֗הּ", "אָ֗הּ"),
            ),
            (
                att("בֹ֜אוּ", "אוּ"),
                att("בֹאוֹ֙", "אוֹ֙"),
                att("רֹאֵ֥י", "אֵ֥י"),
                att("לֹאָ֗הּ", "אָ֗הּ"),
            ),
        ),
        table_classes,
    )
    return table


def _alef_xolam_table_2(bcvi):
    table_classes = (("",) * 3, ("wide-letter-spacing",) * 3)
    table = misc_helpers.en_by_two_table(
        (
            "$roshe9 " + bcv_ref(BK_SONG_OF_SONGS, "7:6", bcvi),
            "$ribot " + bcv_ref(BK_EZRA, "2:69", bcvi),
            "$melot " + bcv_ref(BK_JEREMIAH, "29:10", bcvi),
        ),
        (
            (
                att("רֹאשֵׁ֖ךְ", "רֹא"),
                att("רִבֹּ֣אות", "בֹּ֣אות"),
                att("מְלֹ֧את", "לֹ֧את"),
            ),
            (att("רֹא", "רֹא"), att("בֹּ֣אות", "בֹּ֣אות"), att("לֹ֧את", "לֹ֧את")),
        ),
        table_classes,
    )
    return table
