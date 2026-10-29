from taamey_d.doc.book_codes import BK_DEUTER, BK_ISAIAH, BK_SND_SAMUEL
from taamey_d.doc.book_chapter_verse import bcv, bcv_ref
from taamey_d.doc.html_helpers import anchor, to_str, xheading3, xtable
from taamey_d.doc.html_helpers import xtable_data_cell, xtable_row, xunordered_list


def sec_body(accum, section):
    bcvi = accum, section
    return (
        """
<p>
    $Taamey_D does not claim to be generally applicable.
    Since version 1.1 it is general in one respect:
    each mark below a letter hangs off the mark before it,
    whatever kind either mark is,
    so an accent before a vowel, a second vowel, or two below-accents
    are placed side by side without a rule for the pair.
    The exception is $dexi or $yetiv, which sits at the letter’s right edge:
    another mark below the same letter can still collide with it.
    Beyond that, $Taamey_D supports many words outside its corpus,
    but this support is accidental.
    It often supports its specific corpus through general means,
    leading to this “accidental generality.”
    A concrete example is its support for
    letters with more than one above-accent.
    Excluding $revia_mugrash,
    such letters are rare in the Hebrew Bible
    (in $MAM there are about 20).
    $Taamey_D supports every such case in its corpus,
    and, accidentally, supports many cases outside its corpus.
    It supports those out-of-corpus cases because it was easier to
    support multiple accents in a somewhat general way than
    it would have been to add special-case support for only
    the in-corpus cases.
</p>
<p>Since $Taamey_D’s generality goes no further than that, it might not support words like the following:</p>
<ul>
    <li>$Taamey_D might not support words from editions of the Hebrew Bible that do not closely follow $UXLC or $MAM.
        For example, such words appear in $MAM’s documentation notes, in $MAM’s introduction,
        and in the near-Aleppo edition.
        The near-Aleppo edition has many pointed $ketiv words that $MAM lacks,
        and pointed $ketiv words are a rich source of unusual and even ungrammatical pointing.</li>
    <li>$Taamey_D might not support words with hypothetical cantillation.
        For example, Jacobson’s book on cantillation often shows
        different ways a verse might have been cantillated.
        Such a verse might contain words that are not in any edition of the Hebrew Bible.</li>
    <li>$Taamey_D might not support words from cantillated texts outside the Hebrew Bible.
        For example, here is
        """
        + anchor(_BEN_SIRA_URL, "a recent cantillation of an excerpt from Ben Sira")
        + """.
    </li>
    <li>$Taamey_D might not support words from editions of the Hebrew Bible representing the Masorah parva.
        Those would likely need Masorah circle &amp; combining dot above.
        $Taamey_D centers a Masorah circle over its letter.
        That suffices for the Masorah circles in $MAM’s documentation notes,
        none of which shares its letter with an above-accent.
        $Taamey_D has a glyph for combining dot above, but that glyph’s placement is untested.</li>
</ul>
<p>Texts pointed with only vowels &amp; $meteg
    (i.e. texts without cantillation)
    are unlikely to cause problems for $Taamey_D.
    So, a $siddur is unlikely to cause problems for $Taamey_D.
    A $siddur contains only a few small cantillated passages, and those passages are Biblical.
    Those passages are unlikely to have any words outside $Taamey_D’s corpus.
</p>
"""
        + _beyond_the_bible_text(_add_ssta(bcvi, "beyond the Bible text"))
    )


def _add_ssta(in_bcvi, subsec_title_abbrev):
    accum, section = in_bcvi
    subsection = dict(section, subsec_title_abbrev=subsec_title_abbrev)
    return accum, subsection


def _beyond_the_bible_text(bcvi):
    return (
        to_str(
            xheading3("Words from beyond the Bible text", "h3_beyond_the_bible_text")
        )
        + """
<p>
    Beyond the Bible text of $UXLC and $MAM,
    $Taamey_D’s corpus includes a few phrases from $MAM’s documentation notes
    and one pointed $ketiv word from the near-Aleppo edition.
    They have marks, or combinations of marks, that the Bible text lacks.
    The table below shows some of these words.
</p>
"""
        + _cases_table(bcvi)
        + """
<p>
    Including these few words does not mean that $Taamey_D now handles all words
    in $MAM’s documentation notes, $MAM’s introduction, and the near-Aleppo edition.
    Those texts probably contain many other words that $Taamey_D does not yet render well.
</p>
"""
    )


def _cases_table(bcvi):
    rows = tuple(_case_row(case, bcvi) for case in _CASES)
    header_cells = "Example", "What/Where"
    attrs = {"class": "ruled-rows"}
    return to_str(xtable(header_cells, sum(rows, tuple()), attrs))


def _case_row(case, bcvi):
    hebrew, what, where, book_code, chap_colon_ver, marks = case
    ref = (
        bcv(book_code, chap_colon_ver) + " " + bcv_ref(book_code, chap_colon_ver, bcvi)
    )
    where_ref = where + " " + ref
    if marks:
        what_where = (what + ", in " + where_ref + ", with:", xunordered_list(*marks))
    else:
        what_where = what + " in " + where_ref
    cells = (
        xtable_data_cell(hebrew, {"class": "font-family-taamey-d", "dir": "rtl"}),
        xtable_data_cell(what_where),
    )
    cells2 = tuple((cell, "\n    ") for cell in cells)
    return "\n    ", xtable_row(sum(cells2, tuple()))


_BEN_SIRA_URL = (
    "https://opensiddur.org/readings-and-sourcetexts/mekorot/"
    + "non-canonical/exoteric/second-temple-period/"
    + "paean-of-ben-sira-on-the-merit-of-the-ancestors-chapters-44-50/"
)

_CASES = (
    (
        "הָיִ֛יתָהַ֯ מּ֯וֹצִ֥יא",
        "Masorah circles in the phrase הייתה מוציא",
        "$MAM’s note on",
        BK_SND_SAMUEL,
        "5:2",
        (),
    ),
    (
        "שָׁםָּ֯",
        "A final $mem",
        "$MAM’s note on",
        BK_SND_SAMUEL,
        "21:12",
        ("$qamats under it (!)", "$dagesh in it (!)", "Masorah circle above it"),
    ),
    (
        "לְםַ רְבֵּ֨ה",
        "$Patax under final $mem (!)",
        "$MAM’s note on",
        BK_ISAIAH,
        "9:6",
        (),
    ),
    (
        "וּבַעְּפֹלִ֔ים",
        "$Dagesh in $ayin (!)",
        "$MAM’s note on",
        BK_DEUTER,
        "28:27",
        (),
    ),
    (
        "הִןֵּ֤",
        "A final $nun",
        "the near-Aleppo edition’s pointed $ketiv at",
        BK_ISAIAH,
        "54:16",
        (
            "$dagesh in it (!)",
            "$tsere under it (!) (well, sort of under it)",
            "$mahapa9 under it (!)"
            + " (well, really only conceptually under it;"
            + " in fact sticking way out from it!)",
        ),
    ),
)
