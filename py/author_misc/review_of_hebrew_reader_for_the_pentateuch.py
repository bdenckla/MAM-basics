"""Exports gen_html_file and anchor.

Ported from the Google Doc "WLC Considered Harmful", Ben's review of Kline and
Lavery's A Hebrew Reader for the Pentateuch. Its published copy is
https://docs.google.com/document/d/e/2PACX-1vQ6QyxCbui3JRF2II6QYnF4ZMbjCDXGsQQ3qCheRAKCGvvdp1_TYeXTIiesDNmM-KWxvmW3dlM2ipV8/pub
and the document itself is
https://docs.google.com/document/d/1XV_jIHXSY_qzl0XNLwjBHaw8in9WoFCbyHrN5-7pqow/edit
A throwaway converter generated this module from the document's zip export of
2026-11-08, whose words agreed with the published copy's word for word, so no
prose and no Hebrew was retyped. The prose is verbatim except as listed below.

THE PAGE HAS A SUBTITLE. The h1 is the document's own title. The h2 is the
subtitle Ben chose on 2026-11-08, as urwotm_common.py makes each part's
subtitle the h2 of an urwotm page, so the document's four section headings are
h3. The <title> joins title and subtitle with a colon, in the spelling
without $ keys, since it does not pass through dollar_sub.

THREE SLIPS ARE FIXED, by Ben's decision of 2026-11-08 to fix obvious slips.
Each fix substitutes one named letter for another within one atom:

* "where gray marks the תחלון rather than", in the paragraph that begins "I
  found no documentation in the Reader", has the atom תחתון instead: HEBREW
  LETTER TAV for HEBREW LETTER LAMED.
* "the use of a רפח bar" and "indicating a רפח exclusive", in the paragraph
  that begins "(This is all in 20:12 in some editions.)", have the atom רפה
  instead, the name of the mark: HEBREW LETTER HE for HEBREW LETTER HET.

TWO MORE EDITS ARE BEN'S, made on 2026-11-08 after he read the port:

* in "should have been colored gray (as the מנח and", the atom is now מונח, the
  spelling of the review's four other occurrences of that accent's name, as Ben
  asked: "standardize on the majority spelling".
* in "These errors (and some others like it I will describe separately)", the
  pronoun is now "them", which agrees with "errors", as Ben asked.

TWO HEBREW FORMS ARE REORDERED, NOT REWRITTEN. In both rows of the second
table, the atom תעשה had its sin dot after its segol. MAM-normal mark order
puts the sin dot first (mb_cmn/uni_denorm.py), and by Ben's decision of
2026-10-30, recorded in doc/mam-normal-mark-order.md, a quotation in authored
prose takes that order unless it claims to be byte-accurate. _pointed below
asserts that order for every pointed form here.

FOUR KINDS OF LINK TO RETIRED HOSTS ARE REPOINTED:

* the 18 links to a verse of the retired MAM-with-doc site go to the same page
  and anchor under https://bdenckla.github.io/MAM-basics/MAM-with-doc/;
* footnote 5's link to the review of Chabad's web Tanakh goes to the sibling
  page in this directory;
* the link to section 325 of the adaptation of Yeivin's Introduction goes to
  that section's page under https://bdenckla.github.io/MAM-basics/yeivin-itm/;
* footnote 6's link to Exodus 20 in the Ashkenazic version of Phonetic MAM goes
  to its page under https://bdenckla.github.io/MAM-basics/phonetic-mam/, with
  ?pronunciation=ashkenazic, the form the ArtScroll review's link takes.

Every other link is reproduced as it is.

INVISIBLE CHARACTERS. The document's 143 no-break spaces are ordinary spaces
here, as the urwotm series' importer made them: Google left them at the
boundaries of its spans, not where a line break would be wrong. Its six
left-to-right marks are dropped. Each followed a Hebrew atom that a comma then
followed, in a list of atoms within an English sentence, and gave that comma
the paragraph's left-to-right direction, so that the atoms read in list order.
Here each Hebrew run is a <bdi>, which isolates it, so the comma after it takes
the paragraph's direction without help.

THE REST IS HOUSE STYLE, not rewording:

* the $ keys that dollar_sub requires. BHL has no key and stays bare, as in the
  urwotm series: a $BHL key would make the bare BHL of urwotm parts 1 to 3
  raise.
* the quotation's italic merkha, gaʿya, tevir and shewa are their $ keys, which
  render the same spellings.
* bold is author.emphasis, and the italic titles, the Reader's short title
  included, are author.book_title.
* unpointed Hebrew, which is all the Hebrew of the prose and of the tables'
  labels, is a <bdi> without lang (author.unpointed), in the surrounding font, by
  Ben's decision of 2026-11-08. Only the tables' four pointed forms take
  lang="hbo" and its font (_pointed).
* Google's type sizes are not reproduced, except that the tables' pointed forms
  are big. The gray rows of the tables stay gray (author.span_gray), as the
  document has them.
* each footnote's marker is a link to its note, and the note's marker a link
  back, after he_ws_intro_to_mam_gray_maqaf_1.py's _footnote_marker. A marker
  in the text sits on the baseline rather than raised as in the document, by
  Ben's decision of 2026-11-08: "Superscript footnote callouts create weird
  line spacing." The notes follow a horizontal rule, as in the document.
* each image keeps the width it had on the document's page, at the urwotm
  importer's 40em for Google's 624px, and its file is named for its verse, its
  Hebrew in consensus_to_ascii (py/author_boj_util/author.py) and its source.
"""

from mb_author import author
from mb_cmn import uni_denorm
from mb_misc import mb_html


def anchor():
    return author.std_anchor(_ANCHOR, _H1_CONTENTS)


def gen_html_file(tdm_ch):
    cbody = [
        author.heading_level_1(_H1_CONTENTS),
        author.heading_level_2(_SUBTITLE),
        author.heading_level_3(_H3_INTRO),
        author.para(_INTRO_P01),
        author.para(_INTRO_P02),
        author.para(_INTRO_P03),
        author.para(_INTRO_P04),
        author.para(_INTRO_P05),
        author.para(_INTRO_P06),
        author.para(_INTRO_P07),
        author.para(_INTRO_P08),
        author.para(_INTRO_P09),
        author.para(_INTRO_P10),
        author.para(_INTRO_P11),
        author.ordered_list(_INTRO_OL01),
        author.para(_INTRO_P12),
        author.para(_INTRO_P13),
        author.para(_INTRO_P14),
        author.para(_INTRO_P15),
        author.heading_level_3(_H3_DEFIC),
        author.para(_DEFIC_P01),
        author.para(_DEFIC_P02),
        author.para(_DEFIC_P03),
        author.para(_DEFIC_P04),
        author.para(_DEFIC_P05),
        author.para(_DEFIC_P06),
        author.para_for_img(
            "hebrew_reader/Gen 2v18 A3JH0LV -- LC page F002A.png", width_em=18.9
        ),
        author.para(_DEFIC_P07),
        author.para(_DEFIC_P08),
        author.para(_DEFIC_P09),
        author.blockquote(_DEFIC_QUOTE01),
        author.para(_DEFIC_P10),
        author.para(_DEFIC_P11),
        author.para(_DEFIC_P12),
        author.para(_DEFIC_P13),
        author.para(_DEFIC_P14),
        author.para(_DEFIC_P15),
        author.para(_DEFIC_P16),
        author.para(_DEFIC_P17),
        author.para(_DEFIC_P18),
        author.para_for_img(
            "hebrew_reader/Gen 22v12 MAVMH -- LC page F012A.png", width_em=19.7
        ),
        author.para(_DEFIC_P19),
        author.para(_DEFIC_P20),
        author.para(_DEFIC_P21),
        author.para(_DEFIC_P22),
        author.para_for_img(
            "hebrew_reader/Gen 45v6 VQCYR -- LC page F028A.png", width_em=17.3
        ),
        author.para(_DEFIC_P23),
        author.para(_DEFIC_P24),
        author.para(_DEFIC_P25),
        author.para(_DEFIC_P26),
        author.para(_DEFIC_P27),
        author.para(_DEFIC_P28),
        author.para(_DEFIC_P29),
        author.para(_DEFIC_P30),
        author.para(_DEFIC_P31),
        author.para(_DEFIC_P32),
        author.para(_DEFIC_P33),
        author.para_for_img(
            "hebrew_reader/Exod 20v3 LA_YHYH_L5 -- Hebrew Reader.png", width_em=14.8
        ),
        author.para(_DEFIC_P34),
        author.std_table(_DEFIC_TABLE01, coldirs=_COLDIRS_RTL),
        author.para(_DEFIC_P35),
        author.ordered_list(_DEFIC_OL01),
        author.para(_DEFIC_P36),
        author.ordered_list(_DEFIC_OL02),
        author.para(_DEFIC_P37),
        author.para(_DEFIC_P38),
        author.para(_DEFIC_P39),
        author.para(_DEFIC_P40),
        author.para_for_img(
            "hebrew_reader/Exod 20v4 LA_F3JH_L5 -- Hebrew Reader.png", width_em=17.0
        ),
        author.para(_DEFIC_P41),
        author.std_table(_DEFIC_TABLE02, coldirs=_COLDIRS_RTL),
        author.para(_DEFIC_P42),
        author.para(_DEFIC_P43),
        author.para(_DEFIC_P44),
        author.para(_DEFIC_P45),
        author.para(_DEFIC_P46),
        author.para(_DEFIC_P47),
        author.para(_DEFIC_P48),
        author.para(_DEFIC_P49),
        author.para(_DEFIC_P50),
        author.para(_DEFIC_P51),
        author.para(_DEFIC_P52),
        author.para_for_img(
            "hebrew_reader/Exod 20v8 ZKVR -- Hebrew Reader.png", width_em=5.0
        ),
        author.para(_DEFIC_P53),
        author.para_for_img(
            "hebrew_reader/Exod 20v10 AFH_VBN5_VBF5 -- Hebrew Reader.png", width_em=17.1
        ),
        author.para(_DEFIC_P54),
        author.para(_DEFIC_P55),
        author.para(_DEFIC_P56),
        author.para(_DEFIC_P57),
        author.para(_DEFIC_P58),
        author.para(_DEFIC_P59),
        author.para(_DEFIC_P60),
        author.para(_DEFIC_P61),
        author.para(_DEFIC_P62),
        author.heading_level_3(_H3_CONCL),
        author.para(_CONCL_P01),
        author.para(_CONCL_P02),
        author.para(_CONCL_P03),
        author.heading_level_3(_H3_APPX),
        author.para(_APPX_P01),
        author.ordered_list(_APPX_OL01),
        mb_html.horizontal_rule(),
        _note(1, _NOTE_01),
        _note(2, _NOTE_02),
        _note(3, _NOTE_03),
        _note(4, _NOTE_04),
        _note(5, _NOTE_05),
        _note(6, _NOTE_06),
        _note(7, _NOTE_07),
        _note(8, _NOTE_08),
        _note(9, _NOTE_09),
        _note(10, _NOTE_10),
        _note(11, _NOTE_11),
        _note(12, _NOTE_12),
        _note(13, _NOTE_13),
        _note(14, _NOTE_14),
    ]
    return author.help_gen_html_file(__file__, tdm_ch, _FNAME, _TITLE, cbody)


def _pointed(text):
    """Pointed Hebrew lifted from the document, big, in the pointed-Hebrew font.

    Guarded against a normalizing round trip. MAM-normal mark order gives
    priority to shin dot, sin dot, dagesh/mapiq/shuruq dot, dagesh ḥazaq
    (U+05C9), and rafe. The two dagesh code points share a priority; every other
    mark keeps its relative order. Unicode-normal order sorts by canonical
    combining class instead, which puts a sin dot after the vowel of its letter.
    The two orders render identically, so a paste through anything that
    normalizes is invisible on the page and shows up only where something
    compares bytes. The two forms in the second table arrived in the other
    order, and the module docstring says what was done with them.
    """
    assert uni_denorm.has_std_mark_order(text), text
    return author.hbo_big(text)


def _fn_ref(n):
    """Footnote n's marker in the text: a link to the note, on the baseline.

    Not superscript, as the document has it: a raised marker makes its line
    taller than its neighbours (Ben's decision of 2026-11-08).
    """
    return mb_html.anchor(f"[{n}]", {"id": f"fnref-{n}", "href": f"#fn-{n}"})


def _note(n, contents):
    """Footnote n: its marker, a link back to the text, then the note."""
    marker = mb_html.anchor(f"[{n}]", {"id": f"fn-{n}", "href": f"#fnref-{n}"})
    return author.para([marker, " ", contents])


_SUBTITLE = "A Review of “A Hebrew Reader for the Pentateuch”"
_H1_CONTENTS = "$WLC Considered Harmful"
_TITLE = f"WLC Considered Harmful: {_SUBTITLE}"
_FNAME = "review_of_hebrew_reader_for_the_pentateuch.html"
_ANCHOR = author.anchor_h("document", f"./{_FNAME}")
_COLDIRS_RTL = ("rtl", "rtl")
_READER = author.book_title("Reader")

_URL_WS_MAM = "https://he.wikisource.org/wiki/%D7%9E%D7%A7%D7%A8%D7%90_%D7%A2%D7%9C_%D7%A4%D7%99_%D7%94%D7%9E%D7%A1%D7%95%D7%A8%D7%94#%D7%A8%D7%90%D7%A9"
_URL_UXLC_2021_02_22_1 = "https://tanach.us/Changes/2021.04.01%20-%20Changes/2021.04.01%20-%20Changes.xml?2021.02.22-1"
_URL_MWD_GEN_1_11 = (
    "https://bdenckla.github.io/MAM-basics/MAM-with-doc/A1-Genesis.html#c1v11"
)
_URL_UXLC_2021_02_22_2 = "https://tanach.us/Changes/2021.04.01%20-%20Changes/2021.04.01%20-%20Changes.xml?2021.02.22-2"
_URL_MWD_GEN_2_8 = (
    "https://bdenckla.github.io/MAM-basics/MAM-with-doc/A1-Genesis.html#c2v8"
)
_URL_LC_F002A = "https://manuscripts.sefaria.org/leningrad-color/BIB_LENCDX_F002A.jpg"
_URL_MWD_GEN_2_18 = (
    "https://bdenckla.github.io/MAM-basics/MAM-with-doc/A1-Genesis.html#c2v18"
)
_URL_UXLC_2022_07_02_2 = "https://tanach.us/Changes/2022.10.19%20-%20Changes/2022.10.19%20-%20Changes.xml?2022.07.02-2"
_URL_MWD_GEN_7_19 = (
    "https://bdenckla.github.io/MAM-basics/MAM-with-doc/A1-Genesis.html#c7v19"
)
_URL_MWD_GEN_7_23 = (
    "https://bdenckla.github.io/MAM-basics/MAM-with-doc/A1-Genesis.html#c7v23"
)
_URL_MWD_GEN_15_10 = (
    "https://bdenckla.github.io/MAM-basics/MAM-with-doc/A1-Genesis.html#c15v10"
)
_URL_MWD_GEN_18_15 = (
    "https://bdenckla.github.io/MAM-basics/MAM-with-doc/A1-Genesis.html#c18v15"
)
_URL_UXLC_2024_09_29_1 = "https://tanach.us/Changes/2024.10.19%20-%20Changes/2024.10.19%20-%20Changes.xml?2024.09.29-1"
_URL_YEIVIN_ITM_325 = (
    "https://bdenckla.github.io/MAM-basics/yeivin-itm/yeivin_itm-318_344.html#ns325"
)
_URL_MWD_GEN_22_12 = (
    "https://bdenckla.github.io/MAM-basics/MAM-with-doc/A1-Genesis.html#c22v12"
)
_URL_LC_F012A = "https://manuscripts.sefaria.org/leningrad-color/BIB_LENCDX_F012A.jpg"
_URL_MWD_GEN_32_24 = (
    "https://bdenckla.github.io/MAM-basics/MAM-with-doc/A1-Genesis.html#c32v24"
)
_URL_LC_F028A = "https://manuscripts.sefaria.org/leningrad-color/BIB_LENCDX_F028A.jpg"
_URL_MWD_GEN_45_6 = (
    "https://bdenckla.github.io/MAM-basics/MAM-with-doc/A1-Genesis.html#c45v6"
)
_URL_MWD_EXOD_14_13 = (
    "https://bdenckla.github.io/MAM-basics/MAM-with-doc/A2-Exodus.html#c14v13"
)
_URL_MWD_EXOD_20_2 = (
    "https://bdenckla.github.io/MAM-basics/MAM-with-doc/A2-Exodus.html#c20v2"
)
_URL_UXLC_2021_05_19_8 = "https://tanach.us/Changes/2021.10.19%20-%20Changes/2021.10.19%20-%20Changes.xml?2021.05.19-8"
_URL_MWD_EXOD_20_3 = (
    "https://bdenckla.github.io/MAM-basics/MAM-with-doc/A2-Exodus.html#c20v3"
)
_URL_MWD_EXOD_20_4 = (
    "https://bdenckla.github.io/MAM-basics/MAM-with-doc/A2-Exodus.html#c20v4"
)
_URL_MWD_EXOD_32_17 = (
    "https://bdenckla.github.io/MAM-basics/MAM-with-doc/A2-Exodus.html#c32v17"
)
_URL_MWD_EXOD_33_16 = (
    "https://bdenckla.github.io/MAM-basics/MAM-with-doc/A2-Exodus.html#c33v16"
)
_URL_MWD_NUM_12_9 = (
    "https://bdenckla.github.io/MAM-basics/MAM-with-doc/A4-Numbers.html#c12v9"
)
_URL_UXLC_2023_05_17_1 = "https://tanach.us/Changes/2023.07.04%20-%20Changes/2023.07.04%20-%20Changes.xml?2023.05.17-1"
_URL_UXLC_2022_04_01_5 = "https://tanach.us/Changes/2022.07.04%20-%20Changes/2022.07.04%20-%20Changes.xml?2022.04.01-5"
_URL_UXLC_2022_04_01_6 = "https://tanach.us/Changes/2022.07.04%20-%20Changes/2022.07.04%20-%20Changes.xml?2022.04.01-6"
_URL_UXLC_2022_04_01_7 = "https://tanach.us/Changes/2022.07.04%20-%20Changes/2022.07.04%20-%20Changes.xml?2022.04.01-7"
_URL_UXLC_2022_04_01_9 = "https://tanach.us/Changes/2022.07.04%20-%20Changes/2022.07.04%20-%20Changes.xml?2022.04.01-9"
_URL_UXLC_2022_04_01_10 = "https://tanach.us/Changes/2022.07.04%20-%20Changes/2022.07.04%20-%20Changes.xml?2022.04.01-10"
_URL_UXLC_2022_04_01_17 = "https://tanach.us/Changes/2022.07.04%20-%20Changes/2022.07.04%20-%20Changes.xml?2022.04.01-17"
_URL_UXLC_2022_07_02_21 = "https://tanach.us/Changes/2022.10.19%20-%20Changes/2022.10.19%20-%20Changes.xml?2022.07.02-21"
_URL_CHABAD_CTR = "https://www.chabad.org/torah-texts/63255/Tanakh-The-Hebrew-Bible"
_URL_REVIEW_OF_CTR = "./rocc_0_review_of_ctr.html"
_URL_PHONETIC_MAM_EXOD_20 = "https://bdenckla.github.io/MAM-basics/phonetic-mam/tnkh/A2-Exodus/20.html?pronunciation=ashkenazic"

_H3_INTRO = "Introduction"
_INTRO_P01 = (
    "In recent decades, a common way to make a Hebrew Bible (or some subset of"
    " it) has been to take some version of $WLC and edit, at great expense, from"
    " there. I know that some books used this process because they describe it in"
    " their Foreword or other front matter. For other books, I have inferred this"
    " from places where signs of $WLC have “leaked through” their editing"
    " process."
)
_INTRO_P02 = (
    "Few book projects can afford the Hebrew editing of this process. Though many"
    " parts of publishing have become less expensive, I suspect that Hebrew"
    " editing remains as costly as ever. That would make Hebrew editing more"
    " expensive, relative to the overall budget, than ever before."
)
_INTRO_P03 = (
    "Many projects cannot afford this and have instead resorted to using $WLC"
    " directly (verbatim)."
)
_INTRO_P04 = [
    "One such project was ",
    author.book_title("A Hebrew Reader for the Pentateuch"),
    ", by Kline and Lavery. I will use it as an example of the problems of",
    " “verbatim $WLC” books. Its problems are no worse than those of any other",
    " “verbatim $WLC” book.",
    _fn_ref(1),
    " Nonetheless this ",
    _READER,
    " is a useful example because it is so recent (2024) and because it is so",
    " short.",
]
_INTRO_P05 = [
    "Its recency shows the continued popularity of the “verbatim $WLC” approach",
    " even though something better has been around since 2013: ",
    author.anchor_h("$MAM", _URL_WS_MAM),
    " (",
    author.book_title("Miqra According to the Masorah"),
    "). Though $MAM has existed for more than a decade, it is little-known in the",
    " Jewish publishing world, and almost unknown in the Christian publishing",
    " world.",
    _fn_ref(2),
]
_INTRO_P06 = [
    "Kline and Lavery’s ",
    _READER,
    " is a useful example not only for its recency but also for its brevity. It",
    " contains only 666 numbered verses.",
    _fn_ref(3),
    " Its brevity allows every anomaly inherited from $WLC to be listed. This",
    " list gives a sense of just how dense these anomalies are, if there are so",
    " many even in such a short book.",
    _fn_ref(4),
]
_INTRO_P07 = [
    "$WLC began as a digital version of the body text of $BHS. Over the years, it",
    " diverged from $BHS in places where the $WLC editors found $BHS lacking. But",
    " $WLC remains, like $BHS, a diplomatic edition of the $LC. Therefore it",
    " remains inappropriate for most uses it is put to, including its use in this",
    " ",
    _READER,
    ".",
]
_INTRO_P08 = (
    "The anomalous pointings that one finds in $WLC are relevant only to students"
    " of the $LC itself. They are irrelevant to almost all students of Biblical"
    " Hebrew. When confronted with an anomaly, beginners will probably not know"
    " enough to be confused, but the intermediate student will likely be"
    " “rewarded” with confusion. This is the basic problem with verbatim use of a"
    " diplomatic text like $WLC."
)
_INTRO_P09 = [
    "It is disappointing to see this mistake perpetuated by Hendrickson since its",
    " 2001 BHL (",
    author.book_title("Biblia Hebraica Leningradensia"),
    ") (Dotan) struck a rare balance between the needs of a diplomatic edition",
    " and a general-purpose edition. It did so by embedding, implicitly, a",
    " diplomatic edition inside a general-purpose edition. The main text is a",
    " general-purpose edition that is unobtrusively yet clearly annotated with",
    " pointers to the diplomatic edition implied by its Appendix A.",
]
_INTRO_P10 = [
    "The use of $WLC in this ",
    _READER,
    " contrasts not only with BHL but also with the careful, $AC-centered",
    " approach taken in another Hendrickson book involving Kline: ",
    author.book_title("A Hebrew Reader for the Psalms"),
    " (2021), with Peter Myers. Obviously an $AC-centered approach is not an",
    " option for a Pentateuch reader. My point is that the Psalms ",
    _READER,
    " team invested great effort in the Hebrew text rather than just using $WLC.",
    " No electronic text is better known or less expensive (",
    mb_html.raw_html("$"),
    "0) than $WLC, but it is also a contender for being the least appropriate for",
    " a reader (or even for general-purpose use).",
    _fn_ref(5),
]
_INTRO_P11 = [
    "An arguably more serious problem with diplomatic editions is not the",
    " anomalies they reproduce but the aids they lack. The aids expected in a",
    " reader’s edition depend on whether the target audience is Jewish or",
    " Christian. Roughly speaking, one expects to find pronunciation aids in a",
    " Jewish reader’s edition and one expects to find translation aids in a",
    " Christian reader’s edition. But I see no reason why Christian readers would",
    " not want both types of aids. The pronunciation aids that this ",
    _READER,
    " lacks, at least some of which are present in all Jewish reader’s editions,",
    " are the following:",
]
_INTRO_OL01 = [
    "“Stress helpers” for prepositive and postpositive accents.",
    [
        "A ",
        author.unpointed("קמץ קטן"),
        " symbol distinct from ",
        author.unpointed("קמץ גדול"),
        ".",
    ],
    [
        "A mobile simple ",
        author.unpointed("שווא"),
        " symbol distinct from resting ",
        author.unpointed("שווא"),
        ".",
    ],
    [
        "A ",
        author.unpointed("פסק"),
        " symbol distinct from ",
        author.unpointed("לגרמיה"),
        ". (Not exactly pronunciation.)",
    ],
]
_INTRO_P12 = [
    "A fifth type of aid present in many Jewish reader’s editions ",
    author.emphasis("and"),
    " present in this ",
    _READER,
    " is the separation of the ",
    author.unpointed("תחתון"),
    " cantillation from the ",
    author.unpointed("עליון"),
    " cantillation in the Decalogues. This is not exactly a pronunciation aid; it",
    " is more of a chanting aid.",
    _fn_ref(6),
    " This ",
    _READER,
    ", though presumably not chanting-oriented, has taken pains to reflect, in",
    " its use of whitespace, the prosodic guidance provided by the stronger",
    " disjunctive accents. So it is not entirely surprising that, laudably, the ",
    _READER,
    " does (attempt to) provide the aid of separation of ",
    author.unpointed("תחתון"),
    " from ",
    author.unpointed("עליון"),
    ". Few verbatim-$WLC editions attempt this.",
    _fn_ref(7),
]
_INTRO_P13 = [
    "The ",
    _READER,
    " takes an approach to separation I have not seen before. While it uses the",
    " classic unfriendly approach where ",
    author.unpointed("תחתון"),
    " and ",
    author.unpointed("עליון"),
    " marks appear on a single set of letters, it uses gray for the marks it",
    " deems exclusive to the ",
    author.unpointed("עליון"),
    ", leaving in black the marks it deems either exclusive to the ",
    author.unpointed("תחתון"),
    " or shared by both cantillations.",
    _fn_ref(8),
    " While this approach still leaves some ambiguity (between ",
    author.unpointed("תחתון"),
    " and shared), if it had been carried out with more care it would have been a",
    " big help.",
]
_INTRO_P14 = [
    "On the topic of gray: the halftoning in the ",
    _READER,
    " does not, in my opinion, achieve a convincing emulation of true gray, but",
    " it is good enough. I do not know whether its limitations are simply due to",
    " the resolution of the printing process, or whether the halftoning could",
    " have used the given resolution better. An increase in resolution or a",
    " switch to a genuine two-color printing process would likely be beyond the",
    " budget for this project.",
]
_INTRO_P15 = [
    "Having described, in general terms, what I perceive to be the $WLC-inherited",
    " deficiencies of the ",
    _READER,
    ", I will now catalog some specific examples.",
]
_H3_DEFIC = "$WLC-inherited deficiencies"
_DEFIC_P01 = author.emphasis(
    [
        "In Gn 1:11 ",
        author.unpointed("דשא"),
        ", the ",
        _READER,
        " has ",
        author.unpointed("זקף"),
        " rather than ",
        author.unpointed("רביע"),
        ".",
    ]
)
_DEFIC_P02 = [
    "There is some printed and manuscript precedent for ",
    author.unpointed("זקף"),
    ". But, ",
    author.unpointed("רביע"),
    " is generally agreed to be not only the Masoretic consensus but also the",
    " most likely contents of the $LC there. See ",
    author.anchor_h("$UXLC change 2021.02.22-1", _URL_UXLC_2021_02_22_1),
    " and ",
    author.anchor_h("$MAM with doc", _URL_MWD_GEN_1_11),
    ". Even $BHQ Genesis (2016) has been updated to have ",
    author.unpointed("רביע"),
    " rather than ",
    author.unpointed("זקף"),
    ", though oddly it still has ",
    author.unpointed("זקף"),
    " in its apparatus.",
]
_DEFIC_P03 = [
    author.emphasis(
        [
            "In Gn 2:8 ",
            author.unpointed("גן־בעדן"),
            ", the ",
            _READER,
            " has ",
            author.unpointed("ב"),
            " without ",
            author.unpointed("דגש"),
            ".",
        ]
    ),
    " (page 12)",
]
_DEFIC_P04 = [
    "The $LC’s ",
    author.unpointed("ב"),
    " is most likely free of ",
    author.unpointed("דגש"),
    " (contra ",
    author.anchor_h("$UXLC change 2021.02.22-2", _URL_UXLC_2021_02_22_2),
    "). But whether the $LC has a ",
    author.unpointed("דגש"),
    " here or not is irrelevant; what is relevant is that the consensus is that",
    " there should be a ",
    author.unpointed("דגש"),
    " here. ",
    author.anchor_h("$MAM with doc", _URL_MWD_GEN_2_8),
    " discusses the question of this ",
    author.unpointed("דגש"),
    " as well as other issues with this word.",
]
_DEFIC_P05 = [
    author.emphasis(
        [
            "In Gn 2:18 ",
            author.unpointed("אעשה־לו"),
            ", the ",
            _READER,
            " has a ",
            author.unpointed("דגש"),
            " in the ",
            author.unpointed("ה"),
            ".",
        ]
    ),
    " (page 14)",
]
_DEFIC_P06 = [
    "The $LC is in bad shape here. This is one of its many sections that were",
    " re-inked by a later hand. Nonetheless, the ",
    author.unpointed("דגש"),
    " in question is pretty clear (page ",
    author.anchor_h("2A", _URL_LC_F002A),
    ", column 3, line 5 from the bottom):",
]
_DEFIC_P07 = [
    "Yet, it is also clear that this ",
    author.unpointed("דגש"),
    " is just an anomaly of the $LC (perhaps only present in the re-inked hand),",
    " and thus is inappropriate for a reader’s edition. See the discussion in ",
    author.anchor_h("$MAM with doc", _URL_MWD_GEN_2_18),
    ". (Here and elsewhere, by “anomaly” we mean either an accidental error or an",
    " intentional but nonstandard pointing. For our purposes, it does not matter",
    " which of those two is the source of the anomaly.)",
]
_DEFIC_P08 = [
    author.emphasis(
        [
            "In Gn 7:19 ",
            author.unpointed("גברו"),
            ", the ",
            _READER,
            " has ",
            author.unpointed("געיה"),
            " rather than ",
            author.unpointed("מרכא"),
            " (on ",
            author.unpointed("ג"),
            ").",
        ]
    ),
    " (page 33)",
]
_DEFIC_P09 = [
    "The distinction of ",
    author.unpointed("געיה"),
    " from ",
    author.unpointed("מרכא"),
    " is a vexing problem, particularly in the $LC. Yet, in this case it is",
    " reasonable to apply Dotan’s policy to resolve the problem:",
]
_DEFIC_QUOTE01 = (
    "Since there is usually no unequivocal distinction in the manuscript between"
    " a $merkha and a $gaya_with_half_ring_for_ayin, both being a perpendicular,"
    " straight line underneath the word, we treated this straight line as a"
    " $merkha not only in the accented syllable, but also in a word with $tevir"
    " with no preceding conjunctive accent, when only a mobile $shewa separates"
    " the line from the accent. (Foreword to BHL, page xv)"
)
_DEFIC_P10 = [
    author.anchor_h("$UXLC change 2022.07.02-2", _URL_UXLC_2022_07_02_2),
    " acknowledges this ",
    author.unpointed("מרכא-געיה"),
    " uncertainty with an m-note, though, unlike Dotan, it considers ",
    author.unpointed("געיה"),
    " to be the most likely (or at least the most literal) reading of the $LC. As",
    " usual, ",
    author.anchor_h("$MAM with doc", _URL_MWD_GEN_7_19),
    " discusses the issue.",
]
_DEFIC_P11 = [
    author.emphasis(
        [
            "In Gn 7:23 ",
            author.unpointed("וישאר"),
            ", the ",
            _READER,
            " has ",
            author.unpointed("י"),
            " without ",
            author.unpointed("דגש"),
            ".",
        ]
    ),
    " (page 34)",
]
_DEFIC_P12 = [
    "This lack of ",
    author.unpointed("דגש"),
    " is just an anomaly of the $LC, and thus is inappropriate for a reader’s",
    " edition. See the discussion in ",
    author.anchor_h("$MAM with doc", _URL_MWD_GEN_7_23),
    ".",
]
_DEFIC_P13 = [
    author.emphasis(
        [
            "In Gn 15:10 ",
            author.unpointed("הצפר"),
            ", the ",
            _READER,
            " has ",
            author.unpointed("צ"),
            " without ",
            author.unpointed("דגש"),
            ".",
        ]
    ),
    " (page 52)",
]
_DEFIC_P14 = [
    "Though the Sassoon 1053 manuscript possibly supports it, this lack of ",
    author.unpointed("דגש"),
    " is likely just an anomaly of the $LC, and thus is inappropriate for a",
    " reader’s edition. See the discussion in ",
    author.anchor_h("$MAM with doc", _URL_MWD_GEN_15_10),
    ".",
]
_DEFIC_P15 = [
    author.emphasis(
        [
            "In Gn 18:15 ",
            author.unpointed("ויאמר לא"),
            ", the ",
            _READER,
            " has no ",
            author.unpointed("געיה"),
            " (on ",
            author.unpointed("מ"),
            ").",
        ]
    ),
    " (page 64)",
]
_DEFIC_P16 = [
    "While there is no consensus on this question, an argument can be made (and",
    " is made in ",
    author.anchor_h("$MAM with doc", _URL_MWD_GEN_18_15),
    ") that ",
    author.unpointed("מ"),
    " should have a ",
    author.unpointed("געיה"),
    " in any general-purpose Hebrew Bible. There is even an argument that the $LC",
    " has the remnants of such a ",
    author.unpointed("געיה"),
    ". ",
    author.anchor_h("$UXLC change 2024.09.29-1", _URL_UXLC_2024_09_29_1),
    " interprets these remnants as a ",
    author.unpointed("מרכא"),
    ", albeit with a t-note indicating some uncertainty as to its existence.",
    " While a ",
    author.unpointed("מרכא"),
    " may be the most literal reading of these remnants, I find ",
    author.unpointed("געיה"),
    " rather than ",
    author.unpointed("מרכא"),
    " to be the most likely reading of these remnants. See section 325 of Israel",
    " Yeivin’s ",
    author.book_title("Introduction to the Tiberian Masorah"),
    ", available in a rather freely-adapted version ",
    author.anchor_h("here", _URL_YEIVIN_ITM_325),
    ".",
]
_DEFIC_P17 = [
    author.emphasis(
        [
            "In Gn 22:12 ",
            author.unpointed("מאומה"),
            ", the ",
            _READER,
            " has a ",
            author.unpointed("דגש"),
            " in the second ",
            author.unpointed("מ"),
            ".",
        ]
    ),
    " (page 68)",
]
_DEFIC_P18 = [
    "The $LC pretty clearly has a ",
    author.unpointed("דגש"),
    " in the ",
    author.unpointed("מ"),
    " in question. But that anomaly is irrelevant to a reader’s edition, which",
    " should not have such a ",
    author.unpointed("דגש"),
    ". See ",
    author.anchor_h("$MAM with doc", _URL_MWD_GEN_22_12),
    ". Again, it is irrelevant, but for the curious, here’s an image of the $LC",
    " (page ",
    author.anchor_h("12A", _URL_LC_F012A),
    ", column 2, line 3 from the bottom):",
]
_DEFIC_P19 = [
    author.emphasis(
        [
            "In Gn 32:24 ",
            author.unpointed("את־אשר־לו"),
            ", the ",
            _READER,
            " lacks a ",
            author.unpointed("סילוק"),
            ".",
        ]
    ),
    " (page 80)",
]
_DEFIC_P20 = [
    "The ",
    author.unpointed("סילוק"),
    " is expected on ",
    author.unpointed("ל"),
    ". This is likely an accidental error in the $LC, not an intentional but",
    " nonstandard (lack of) pointing. Those wishing to speculate to the contrary",
    " have many diplomatic versions of the $LC to work from, as well as the",
    " blessing of Internet-available color photos, something previous generations",
    " of scholars could only dream of. (And even such dreams would have required",
    " an almost prophetic imagination.) In short, there is no reason to pollute a",
    " reader’s edition with such an anomaly. See ",
    author.anchor_h("$MAM with doc", _URL_MWD_GEN_32_24),
    ". A ",
    author.unpointed("סילוק"),
    " is similarly missing in the ",
    _READER,
    " in Ex 32:17. See below.",
]
_DEFIC_P21 = [
    author.emphasis(
        [
            "In Gn 45:6 ",
            author.unpointed("וקציר"),
            ", the ",
            _READER,
            " has a ",
            author.unpointed("דגש"),
            " in the ",
            author.unpointed("צ"),
            ".",
        ]
    ),
    " (page 89)",
]
_DEFIC_P22 = [
    "The $LC pretty clearly has a ",
    author.unpointed("דגש"),
    " on the ",
    author.unpointed("צ"),
    " in question (page ",
    author.anchor_h("28A", _URL_LC_F028A),
    ", column 2, 3 lines up from the bottom):",
]
_DEFIC_P23 = [
    "But, as usual, whether the ",
    author.unpointed("דגש"),
    " is clear or not is irrelevant. It is anomalous. See ",
    author.anchor_h("$MAM with doc", _URL_MWD_GEN_45_6),
    ".",
]
_DEFIC_P24 = [
    author.emphasis(
        [
            "In Ex 14:13 ",
            author.unpointed("התיצבו"),
            ", the ",
            _READER,
            " has ",
            author.unpointed("צ"),
            " without ",
            author.unpointed("דגש"),
            ".",
        ]
    ),
    " (page 111)",
]
_DEFIC_P25 = [
    "This reflects an anomaly in the $LC. See ",
    author.anchor_h("$MAM with doc", _URL_MWD_EXOD_14_13),
    ".",
]
_DEFIC_P26 = author.emphasis(
    [
        "In Ex 20:2, the ",
        _READER,
        " fully reverses ",
        author.unpointed("תחתון"),
        " and ",
        author.unpointed("עליון"),
        ".",
    ]
)
_DEFIC_P27 = [
    "These errors (and some others like them I will describe separately) do not",
    " directly stem from $WLC since it makes no distinction between ",
    author.unpointed("תחתון"),
    " and ",
    author.unpointed("עליון"),
    ". They stem indirectly from $WLC in the sense that because it provides no",
    " help, the editors of the ",
    _READER,
    " had to “go it alone,” an error-prone enterprise. I will merely list the",
    " four words involved, without getting into the details: ",
    author.unpointed("אנכי … אלהיך … מבית עבדים"),
    ". Not only the ",
    author.unpointed("סילוק"),
    " of ",
    author.unpointed("עבדים"),
    " but also its ",
    author.unpointed("סוף פסוק"),
    " should be gray. I.e. the span of words between the ",
    author.unpointed("ב"),
    " and ",
    author.unpointed("ג"),
    " verse numerals in the ",
    _READER,
    " should be notated as a complete chanted verse only in the ",
    author.unpointed("עליון"),
    ". In the ",
    author.unpointed("תחתון"),
    ", this span of words is merely a half-verse, i.e. reaches merely up to the ",
    author.unpointed("אתנח"),
    ".",
]
_DEFIC_P28 = "A similar full reversal of the cantillations happens in 20:13–15."
_DEFIC_P29 = [
    "I found no documentation in the ",
    _READER,
    " of what gray is supposed to mean, and have simply inferred that it is",
    " supposed to mark the ",
    author.unpointed("עליון"),
    ". In an alternate interpretation, where gray marks the ",
    author.unpointed("תחתון"),
    " rather than the ",
    author.unpointed("עליון"),
    ", these four verses (20:2, 13–15) would be correct, and all other verses",
    " having dual cantillation would be wrong.",
]
_DEFIC_P30 = author.emphasis(
    ["In Ex 20, the ", _READER, " has multiple anomalous accent orderings."]
)
_DEFIC_P31 = [
    "In the Exodus Decalogue, when there are two below-accents or two",
    " above-accents on a letter, the $LC often frustrates expectations of ",
    author.unpointed("תחתון"),
    "-then-",
    author.unpointed("עליון"),
    " ordering. While the ",
    _READER,
    "’s use of gray makes these anomalies mostly harmless, I still see no reason",
    " to reproduce them in a reader’s edition. One early example is the $LC’s ",
    author.unpointed("פזר"),
    "-then-",
    author.unpointed("זקף"),
    " ordering on ",
    author.unpointed("תמונה"),
    " in 20:4.",
    _fn_ref(9),
    " This is ",
    author.unpointed("עליון"),
    "-then-",
    author.unpointed("תחתון"),
    " ordering, i.e. the anomalous ordering, which shows up in the ",
    _READER,
    " as gray-then-black ordering. I will not list other examples. There are",
    " several.",
]
_DEFIC_P32 = [
    author.emphasis(
        [
            "In Ex 20:3 ",
            author.unpointed("לא יהיה לך"),
            ", the ",
            _READER,
            "’s ",
            author.unpointed("תחתון"),
            " and ",
            author.unpointed("עליון"),
            " are anomalous.",
        ]
    ),
    " (page 134)",
]
_DEFIC_P33 = [
    "(This is in 20:2 in some editions.) In its representation of the two",
    " cantillations of the three “atoms” ",
    author.unpointed("לא"),
    ", ",
    author.unpointed("יהיה"),
    ", and ",
    author.unpointed("לך"),
    ", the ",
    _READER,
    " lacks two marks and colors two marks wrong.",
]
_DEFIC_P34 = "The full, consensus cantillations are as follows."
_DEFIC_TABLE01 = [
    [
        author.span_gray(_pointed("לֹ֣א יִהְיֶֽה־לְךָ֩")),
        author.unpointed("(עליון)"),
    ],
    [
        _pointed("לֹֽא־יִהְיֶ֥ה לְךָ֛"),
        author.unpointed("(תחתון)"),
    ],
]
_DEFIC_P35 = [
    "The ",
    _READER,
    " lacks the following two marks, presumably because they are absent from the",
    " $WLC (and absent from the $LC itself):",
]
_DEFIC_OL01 = [
    [
        "The ",
        _READER,
        " lacks the ",
        author.unpointed("מקף"),
        " after ",
        author.unpointed("לא"),
        " in the ",
        author.unpointed("תחתון"),
        ". (Had the ",
        _READER,
        " added this ",
        author.unpointed("מקף"),
        ", it would suffer from the shared vs ",
        author.unpointed("תחתון"),
        " ambiguity of the ",
        _READER,
        "’s scheme.)",
    ],
    [
        "The ",
        _READER,
        " lacks ",
        author.unpointed("מרכא"),
        " on ",
        author.unpointed("יהיה"),
        " in the ",
        author.unpointed("תחתון"),
        ". (That is, unless the ",
        _READER,
        " makes deliberate but inadvisable use of ",
        author.unpointed("מרכא-געיה"),
        " uncertainty, letting a single stroke stand for both marks.)",
    ],
]
_DEFIC_P36 = [
    "The following two marks are exclusive to the ",
    author.unpointed("עליון"),
    " and therefore, according to the ",
    _READER,
    "’s scheme, should have been colored gray (as the ",
    author.unpointed("מונח"),
    " and ",
    author.unpointed("תלישא"),
    " were) rather than black:",
]
_DEFIC_OL02 = [
    [
        "The ",
        author.unpointed("געיה"),
        " should have been gray. (That is, unless the ",
        _READER,
        " makes deliberate but inadvisable use of ",
        author.unpointed("מרכא-געיה"),
        " uncertainty, letting a single stroke stand for both marks. In that case the",
        " ",
        author.unpointed("געיה"),
        " is shared and therefore is already correctly colored (black).)",
    ],
    [
        "The ",
        author.unpointed("מקף"),
        " after ",
        author.unpointed("יהיה"),
        " should have been gray. See ",
        author.anchor_h("$MAM with doc", _URL_MWD_EXOD_20_2),
        ".",
    ],
]
_DEFIC_P37 = author.emphasis(
    [
        "In Ex 20:3 ",
        author.unpointed("פני"),
        ", the ",
        _READER,
        "’s ",
        author.unpointed("פתח"),
        " appears to belong to the ",
        author.unpointed("י"),
        ".",
    ]
)
_DEFIC_P38 = [
    "(This is in 20:2 in some editions.) This is a mistake in $BHS inherited by",
    " $WLC, not an anomaly in the $LC itself. See $UXLC change ",
    author.anchor_h("2021.05.19-8", _URL_UXLC_2021_05_19_8),
    ". Typographically, this is a challenging word, but something should be done",
    " to suggest that the ",
    author.unpointed("פתח"),
    " belongs to the ",
    author.unpointed("נ"),
    ".",
]
_DEFIC_P39 = [
    author.emphasis(
        [
            "In Ex 20:4 ",
            author.unpointed("לא תעשה לך"),
            ", the ",
            _READER,
            "’s ",
            author.unpointed("תחתון"),
            " and ",
            author.unpointed("עליון"),
            " are anomalous.",
        ]
    ),
    " (page 135)",
]
_DEFIC_P40 = [
    "(This is 20:3 in some editions.) In its representation of the two",
    " cantillations of the three “atoms” ",
    author.unpointed("לא"),
    ", ",
    author.unpointed("תעשה"),
    ", and ",
    author.unpointed("לך"),
    ", the ",
    _READER,
    " lacks one mark, colors two marks wrong, and, arguably, misplaces one mark.",
]
_DEFIC_P41 = "The full, consensus cantillations are as follows."
_DEFIC_TABLE02 = [
    [
        author.span_gray(_pointed("לֹ֣א תַעֲשֶֽׂה־לְךָ֣")),
        author.unpointed("(עליון)"),
    ],
    [
        _pointed("לֹֽא־תַעֲשֶׂ֨ה לְךָ֥"),
        author.unpointed("(תחתון)"),
    ],
]
_DEFIC_P42 = [
    "As above in ",
    author.unpointed("לא יהיה לך"),
    ", here in ",
    author.unpointed("לא תעשה לך"),
    " the ",
    _READER,
    " lacks the ",
    author.unpointed("מקף"),
    " after ",
    author.unpointed("לא"),
    " in the ",
    author.unpointed("תחתון"),
    ", reproducing an anomaly (or at least, a regrettably implicit notation) in",
    " the $LC (via $WLC).",
]
_DEFIC_P43 = [
    "Also as above, the ",
    _READER,
    " should have used gray for two marks on ",
    author.unpointed("תעשה"),
    ": the ",
    author.unpointed("מקף"),
    " after it and its ",
    author.unpointed("געיה"),
    ", wherever that ",
    author.unpointed("געיה"),
    " is located (see below).",
]
_DEFIC_P44 = [
    "The ",
    _READER,
    ", like several estimable (but in my opinion mistaken) modern printed",
    " editions, reproduces an anomalous location for the ",
    author.unpointed("געיה"),
    " on ",
    author.unpointed("תעשה"),
    " in the ",
    author.unpointed("עליון"),
    ", namely, on the ",
    author.unpointed("ת"),
    ". The consensus formed from consulting other manuscripts is that this ",
    author.unpointed("געיה"),
    " should be on the ",
    author.unpointed("ש"),
    ", the letter where, not coincidentally, the $qadma is in the ",
    author.unpointed("תחתון"),
    ". The $LC’s own Deuteronomy Decalogue supports this consensus as well. See ",
    author.anchor_h("$MAM with doc", _URL_MWD_EXOD_20_3),
    ".",
]
_DEFIC_P45 = author.emphasis(
    [
        "In Ex 20:4 ",
        author.unpointed("בארץ מתחת"),
        ", the ",
        _READER,
        "’s ",
        author.unpointed("פתח"),
        " (on ",
        author.unpointed("ת"),
        ") should be gray.",
    ]
)
_DEFIC_P46 = [
    "(This is 20:3 in some editions.) The ",
    author.unpointed("פתח"),
    " here should be colored gray, as it is, correctly, in Ex 20:3 ",
    author.unpointed("פני"),
    ". (There the ",
    author.unpointed("פתח"),
    " belongs to the wrong letter but has the right color (gray).)",
]
_DEFIC_P47 = author.emphasis(
    [
        "In Ex 20:4 ",
        author.unpointed("ואשר במים"),
        ", the ",
        _READER,
        " has ",
        author.unpointed("מונח"),
        " in the ",
        author.unpointed("עליון"),
        ".",
    ]
)
_DEFIC_P48 = [
    "(This is 20:3 in some editions.) Arguably, the consensus is that both ",
    author.unpointed("תחתון"),
    " and ",
    author.unpointed("עליון"),
    " have ",
    author.unpointed("מרכא"),
    ". See ",
    author.anchor_h("$MAM with doc", _URL_MWD_EXOD_20_3),
    ".",
]
_DEFIC_P49 = [
    author.emphasis(
        [
            "In Ex 20:5 ",
            author.unpointed("לא־תשתחוה"),
            ", the ",
            _READER,
            " has a simple ",
            author.unpointed("שווא"),
            " on ",
            author.unpointed("ח"),
            ".",
        ]
    ),
    " (page 135)",
]
_DEFIC_P50 = [
    "(This is 20:4 in some editions.) The consensus pointing is ",
    author.unpointed("חטף פתח"),
    " on ",
    author.unpointed("ח"),
    ". See ",
    author.anchor_h("$MAM with doc", _URL_MWD_EXOD_20_4),
    ".",
]
_DEFIC_P51 = author.emphasis(
    [
        "In Ex 20:10 ",
        author.unpointed("אתה ובנך ובתך"),
        ", the ",
        _READER,
        "’s ",
        author.unpointed("לגרמיה"),
        " is ambiguous.",
    ]
)
_DEFIC_P52 = [
    "(This is 20:9 in some editions.) Mostly, the ",
    _READER,
    " gets away with using black for both ",
    author.unpointed("תחתון"),
    " and shared symbols. It gets away with it because most black symbols that",
    " are exclusive to the ",
    author.unpointed("תחתון"),
    " have a gray symbol that the astute reader can identify as excluding that",
    " black symbol from the ",
    author.unpointed("עליון"),
    ". In such cases, it is clear to the astute reader that we are dealing with",
    " an “either/or” situation. For instance even in 20:8 ",
    author.unpointed("זכור"),
    ",",
    _fn_ref(10),
    " though the accents are not vying for the same letter, the astute reader can",
    " identify that the gray ",
    author.unpointed("תלישא"),
    " excludes the black ",
    author.unpointed("תביר"),
    " from the ",
    author.unpointed("עליון"),
    ":",
]
_DEFIC_P53 = [
    "But it takes a real expert, not just an astute reader, to identify that,",
    " though the ",
    author.unpointed("מונח"),
    " on ",
    author.unpointed("אתה"),
    " is shared, the ",
    author.unpointed("תלישא"),
    " in ",
    author.unpointed("ובנך"),
    " excludes the ",
    author.unpointed("לגרמיה"),
    " from the ",
    author.unpointed("עליון"),
    " in the following:",
]
_DEFIC_P54 = [
    "I.e. the ",
    author.unpointed("תחתון"),
    " has ",
    author.unpointed("מונח לגרמיה"),
    " whereas the ",
    author.unpointed("עליון"),
    " merely has ",
    author.unpointed("מונח"),
    ". As far as I can see, the ",
    _READER,
    " has no way to notate that within its scheme of gray and black.",
]
_DEFIC_P55 = author.emphasis(
    [
        "In Ex 20:13–15, the ",
        _READER,
        " fully reverses ",
        author.unpointed("תחתון"),
        " and ",
        author.unpointed("עליון"),
        ".",
    ]
)
_DEFIC_P56 = [
    "(This is all in 20:12 in some editions.) These are the distinctively-short",
    " verses of the ",
    author.unpointed("עליון"),
    ", that should each be cantillated with ",
    author.unpointed("טפחא"),
    " and ",
    author.unpointed("סילוק"),
    ". A similar full reversal of the cantillations happens in 20:2. The ",
    author.unpointed("דגש"),
    " marks inside of each of the following words should have been gray since",
    " they belong only to the ",
    author.unpointed("עליון"),
    ": verse 13 ",
    author.unpointed("תרצח"),
    ", verse 14 ",
    author.unpointed("תנאף"),
    ", and verse 15 ",
    author.unpointed("תגנב"),
    ". It is unclear whether, pragmatically, a mark as tiny as a ",
    author.unpointed("דגש"),
    " can be recognized to be gray, particularly with the not-very-convincing",
    " halftoning of this volume. It is possible that the use of a ",
    author.unpointed("רפה"),
    " bar in black above each of these letters might help, indicating a ",
    author.unpointed("רפה"),
    " exclusive to the ",
    author.unpointed("תחתון"),
    ".",
]
_DEFIC_P57 = [
    author.emphasis(
        [
            "In Ex 32:17 ",
            author.unpointed("במחנה"),
            ", the ",
            _READER,
            " lacks a ",
            author.unpointed("סילוק"),
            ".",
        ]
    ),
    " (page 150)",
]
_DEFIC_P58 = [
    "The ",
    author.unpointed("סילוק"),
    " is expected on ",
    author.unpointed("נ"),
    ". As in Gn 32:24, this is likely an accidental error in the $LC, and thus",
    " unlikely to be even of scholarly interest. But, as usual, the source of the",
    " anomaly is irrelevant: even anomalies of scholarly interest have no place",
    " in a reader’s edition. Unlike the Gn 32:24 case, there is a ",
    author.unpointed("געיה"),
    " on the word, which makes the lack of ",
    author.unpointed("סילוק"),
    " more dangerous, since the ",
    author.unpointed("געיה"),
    " could be taken to be a ",
    author.unpointed("סילוק"),
    " by an inexperienced reader. See ",
    author.anchor_h("$MAM with doc", _URL_MWD_EXOD_32_17),
    ".",
]
_DEFIC_P59 = [
    author.emphasis(
        [
            "In Ex 33:16 ",
            author.unpointed("ונפלינו"),
            ", the ",
            _READER,
            " has ",
            author.unpointed("צירה"),
            " on ",
            author.unpointed("ל"),
            ".",
        ]
    ),
    " (page 157)",
]
_DEFIC_P60 = [
    "The consensus pointing is ",
    author.unpointed("חיריק"),
    ". See ",
    author.anchor_h("$MAM with doc", _URL_MWD_EXOD_33_16),
    ".",
]
_DEFIC_P61 = [
    author.emphasis(
        [
            "In Nm 12:9 ",
            author.unpointed("ויחר אף"),
            ", the ",
            _READER,
            " lacks a ",
            author.unpointed("מקף"),
            ".",
        ]
    ),
    " (page 178)",
]
_DEFIC_P62 = [
    "This leaves ",
    author.unpointed("ויחר"),
    " with no accent, only a ",
    author.unpointed("געיה"),
    ", which, as one might imagine, is not the consensus pointing of this word.",
    " See ",
    author.anchor_h("$MAM with doc", _URL_MWD_NUM_12_9),
    ". The ",
    _READER,
    " represents some but not all the $LC anomalies in these words/this word. See",
    " the Appendix of this review.",
]
_H3_CONCL = "Conclusion"
_CONCL_P01 = [
    "The ",
    _READER,
    " should have used a base text like $MAM, which reflects the Masoretic",
    " consensus or, in dubious cases, at least reflects its editors’ best,",
    " educated guess as to the Masoretic consensus. Instead, the ",
    _READER,
    " used $WLC, which merely reflects the $LC, or, in dubious cases, reflects",
    " its editors’ best, educated guess as to the contents of the $LC.",
]
_CONCL_P02 = [
    "The $LC contains many anomalies that may confuse or mislead students.",
    " Beginners are likely to be misled; intermediate students may know enough to",
    " be confused. While the unexpected presence or absence of a ",
    author.unpointed("דגש"),
    " here and there does no great harm, there is no reason to accept these",
    " anomalies, and many other editions outside the “cult of $BHS” do better,",
    " including $MAM and Hendrickson’s own BHL and Psalms ",
    _READER,
    ". In rare cases, such as a missing ",
    author.unpointed("סילוק"),
    " on a word with a ",
    author.unpointed("געיה"),
    ",",
    _fn_ref(11),
    " the harm is greater than in the more typical ",
    author.unpointed("דגש"),
    "-related cases.",
]
_CONCL_P03 = [
    "The ",
    _READER,
    " attempted to impose a “gray for ",
    author.unpointed("עליון"),
    "” reading aid upon the unfriendly $WLC base text for the Exodus Decalogue.",
    " Though the attempt was laudable, its many serious errors made it, overall,",
    " a failure. The use of a base text like $MAM, which supplies separated ",
    author.unpointed("תחתון"),
    " and ",
    author.unpointed("עליון"),
    " Decalogues, would have avoided such a failure.",
]
_H3_APPX = "Appendix: Felicitous failures of $BHS"
_APPX_P01 = [
    "Fortunately for Kline and Lavery, $WLC, despite its occasional corrections",
    " to $BHS, inherits some of the felicitous failures of $BHS. $BHS strives to",
    " be a diplomatic edition of the $LC, but often fails to do so. When $BHS",
    " accidentally reflects the Masoretic consensus instead of an anomaly in the",
    " $LC, this makes the ",
    _READER,
    " accidentally more appropriate for general-purpose use, as long as $WLC has",
    " not corrected the error in $BHS. I found that this happened in the ",
    _READER,
    " in the following cases:",
]
_APPX_OL01 = [
    [
        "In Gn 16:2 ",
        author.unpointed("ממנה"),
        ", there is strong evidence for the two dots that would make an anomalous ",
        author.unpointed("צירה"),
        ". There is little or no evidence of a third, centered, lower dot that would",
        " make the consensus ",
        author.unpointed("סגול"),
        ". Luckily, $WLC fails to reflect that anomaly. See $UXLC change ",
        author.anchor_h("2023.05.17-1", _URL_UXLC_2023_05_17_1),
        ".",
    ],
    [
        "In Ex 14:9 ",
        author.unpointed("וישיגו"),
        ", the $LC lacks ",
        author.unpointed("דגש"),
        " in ",
        author.unpointed("ש"),
        ". Luckily, $WLC fails to reflect that anomaly. See ",
        author.anchor_h("$UXLC change 2022.04.01-5", _URL_UXLC_2022_04_01_5),
        ".",
    ],
    [
        "In Ex 16:9 ",
        author.unpointed("ויאמר"),
        ", the $LC lacks ",
        author.unpointed("דגש"),
        " in ",
        author.unpointed("י"),
        ". Luckily, $WLC fails to reflect that anomaly. See ",
        author.anchor_h("$UXLC change 2022.04.01-6", _URL_UXLC_2022_04_01_6),
        ".",
    ],
    [
        "In Ex 16:29, 20:8,",
        _fn_ref(12),
        " and 20:11",
        _fn_ref(13),
        " ",
        author.unpointed("השבת"),
        ", the $LC lacks ",
        author.unpointed("דגש"),
        " in ",
        author.unpointed("ש"),
        ". Luckily, $WLC fails to reflect those anomalies. See $UXLC changes ",
        author.anchor_h("2022.04.01-7", _URL_UXLC_2022_04_01_7),
        ", ",
        author.anchor_h("2022.04.01-9", _URL_UXLC_2022_04_01_9),
        ", and ",
        author.anchor_h("2022.04.01-10", _URL_UXLC_2022_04_01_10),
        ".",
    ],
    [
        "See above regarding Ex 20:8 ",
        author.unpointed("השבת"),
        ".",
    ],
    [
        "See above regarding Ex 20:11 ",
        author.unpointed("השבת"),
        ".",
    ],
    [
        "In Ex 20:10",
        _fn_ref(14),
        " ",
        author.unpointed("אלהיך"),
        ", the $LC appears to have two ",
        author.unpointed("אתנח"),
        " marks, one before (!) the ",
        author.unpointed("סגול"),
        " on ",
        author.unpointed("ה"),
        " and one in the expected location, after that ",
        author.unpointed("סגול"),
        ". Luckily, $WLC fails to reflect that anomaly.",
    ],
    [
        "In Ex 32:19 ",
        author.unpointed("וישבר"),
        ", the $LC has ",
        author.unpointed("דגש"),
        " in ",
        author.unpointed("י"),
        ". Luckily, $WLC fails to reflect that anomaly. See $UXLC change ",
        author.anchor_h("2022.04.01-17", _URL_UXLC_2022_04_01_17),
        ".",
    ],
    [
        "In Nm 12:9 ",
        author.unpointed("ויחר אף"),
        ", the $LC has a simple ",
        author.unpointed("שווא"),
        " on ",
        author.unpointed("ר"),
        ", indicating that these six letters form a single non-compound word: ",
        author.unpointed("ויחראף"),
        ". Luckily, $WLC fails to reflect both the anomalous ",
        author.unpointed("שווא"),
        " and the six-letter word that it implies. Unluckily, $WLC does reflect the",
        " $LC’s lack of a ",
        author.unpointed("מקף"),
        " joining ",
        author.unpointed("ויחר"),
        " and ",
        author.unpointed("אף"),
        ", giving these letters a “worst of both worlds” mix of both poor fidelity to",
        " the $LC and nonconformance with the Masoretic consensus. See $UXLC change ",
        author.anchor_h("2022.07.02-21", _URL_UXLC_2022_07_02_21),
        ".",
    ],
]
_NOTE_01 = [
    "E.g., Zondervan’s 2008 ",
    _READER,
    ".",
]
_NOTE_02 = (
    "$MAM’s obscurity is as much (or more) due to my failure to promote it as it"
    " is others’ failure to seek it out."
)
_NOTE_03 = [
    "Note that numbered verses do not necessarily correspond to chanted verses.",
    " E.g. the span of text labelled by a verse number may contain more than one",
    " or less than one chanted ",
    author.unpointed("סוף פסוק"),
    ". Also note that the number of chanted verses is not well defined in the ",
    _READER,
    " because it has a dually-cantillated passage (the Exodus Decalogue). Note",
    " that according to the list on pages xvi and xvii, the ",
    _READER,
    " has only 665 verses. This is because section 2.6, “Jacob’s Ladder,” Gen",
    " 28:10-22, is incorrectly identified as having only 12 verses. (It has 13.)",
]
_NOTE_04 = (
    "This assumes that anomalies are evenly distributed across Tanakh; that is"
    " probably not true, but may be close enough to true to still make this a"
    " valid point."
)
_NOTE_05 = [
    "The ",
    author.anchor_h("Chabad-hosted $CTR", _URL_CHABAD_CTR),
    " (Judaica Press) is the only electronic text I am aware of that would be a",
    " worse choice. See ",
    author.anchor_h("my review", _URL_REVIEW_OF_CTR),
    ".",
]
_NOTE_06 = [
    "Although cantillation separation is not primarily a pronunciation aid, many",
    " people are unaware that the cantillations cause ",
    author.unpointed("דגש"),
    " and vowel differences in some places. I.e., the differences between the",
    " cantillations are not limited to the accents and the marks most closely",
    " associated with the accents (",
    author.unpointed("געיה"),
    ", ",
    author.unpointed("מקף"),
    ", ",
    author.unpointed("פסק"),
    ", ",
    author.unpointed("לגרמיה"),
    ", and ",
    author.unpointed("סוף פסוק"),
    "). But, the ",
    author.unpointed("דגש"),
    " and vowel differences in question will not result in different",
    " pronunciations for some Hebrew readers. The ",
    author.unpointed("דגש"),
    " differences are on the letter ",
    author.unpointed("ת"),
    ", which, for some readers, is pronounced the same whether or not it has a ",
    author.unpointed("דגש קל"),
    ". Similarly, the vowel differences are between ",
    author.unpointed("קמץ גדול"),
    " and ",
    author.unpointed("פתח"),
    ", which, for some readers, are pronounced the same. Note, though, that there",
    " are living readers who ",
    author.emphasis("do"),
    " make both of these distinctions in pronunciation. See ",
    author.anchor_h("Exodus 20", _URL_PHONETIC_MAM_EXOD_20),
    " in the Ashkenazic version of my Phonetic $MAM.",
]
_NOTE_07 = [
    "Editions that do not separate the cantillations could be doing so by",
    " conscious (but in my opinion poor) editorial choice, or they could simply",
    " be unaware of the option to separate. For example, Zondervan’s ",
    _READER,
    " does not attempt separation, but it is hard to know whether this was a",
    " conscious choice or an accident. Timothy Lee’s ",
    author.book_title("The Book of Deuteronomy: A Hebrew Reader"),
    ", another verbatim-$WLC edition, attempts to present only the ",
    author.unpointed("תחתון"),
    " but does an incomplete job of it.",
]
_NOTE_08 = [
    "This “",
    author.unpointed("עליון"),
    " in gray” scheme is reversed in Exodus verses 20:2 and 13–15. There it is",
    " the ",
    author.unpointed("תחתון"),
    " that is in gray.",
]
_NOTE_09 = "In some editions this is 20:3 not 20:4."
_NOTE_10 = "In some editions this is 20:7 not 20:8."
_NOTE_11 = [
    "Ex 32:17 ",
    author.unpointed("במחנה"),
    ".",
]
_NOTE_12 = "In some editions this is 20:7 not 20:8."
_NOTE_13 = "In some editions this is 20:10 not 20:11."
_NOTE_14 = "In some editions this is 20:9 not 20:10."
