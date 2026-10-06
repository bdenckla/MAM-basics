"""Describe near-Aleppo's template, representation and reading differences from MAM.

doc_page.py assembles these sections. Counts come from the asserted population
snapshot through doc_html.Numbers. Named examples are checked against source
templates or snapshot site lists, and preserve their source attribution.
"""

from near_aleppo.doc_html import he_name
from near_aleppo.doc_html import itm
from near_aleppo.doc_html import link
from near_aleppo.doc_html import table
from near_aleppo.doc_html import verse_key
from near_aleppo.doc_html import verse_refs
from near_aleppo.doc_html import HEBREW_CELL
from near_aleppo.doc_html import NUMBER_CELL
from mb_misc import mb_html
from near_aleppo import doc_he_transfer
from near_aleppo import doc_daniel_sheva
from near_aleppo import doc_genesis_ketiv
from near_aleppo import doc_template_examples
from near_aleppo import doc_policy_examples
from near_aleppo.phase2_templates import MARKS_WITHOUT_LETTER
from near_aleppo.phase2_templates import POINTED_KETIV_PARAMETER
from near_aleppo.phase2_templates import TEMPLATES_ABSENT_FROM_DATASET
from near_aleppo.phase2_templates import _KEPT_LARGE_LETTER_VERSE
from near_aleppo.phase3_policies import _ADONAI_LETTERS

SECTION = ("what-the-dataset-changes", "What near-Aleppo changes")
TEMPLATES = ("templates", "MAM's templates: evaluated away or kept")
QAMATS = ("qamats-size", "The qamats size")
DIVINE_NAME = ("divine-name-holam", "The holam in the divine name")
DIVINE_TITLE = ("divine-title-holam", "The holam in the divine title")
ELOHIM = ("elohim-vowel", "The divine name read Elohim")
REVIA = ("revia-mugrash", "The revia mugrash")
OLE = ("ole-and-yored", "The ole on the yored's letter")
KETIV_QERE = ("ketiv-qere-apparatus", "The ketiv/qere apparatus")
MAQAF = ("maqaf", "The maqaf")
HATAF = ("hataf", "The hataf on a letter that is not a guttural")
STRESS = ("stress-helpers", "The stress helpers")
READINGS = ("codex-readings", "The codex's readings in MAM's notes")
POINTED_KETIV = ("pointed-ketiv", "The pointed ketiv")
SUBSECTIONS = (
    TEMPLATES,
    QAMATS,
    DIVINE_NAME,
    DIVINE_TITLE,
    ELOHIM,
    REVIA,
    OLE,
    KETIV_QERE,
    MAQAF,
    HATAF,
    STRESS,
    READINGS,
    POINTED_KETIV,
)

_P2 = "phase2_counts"
_P3 = "phase3_counts"
_P3S = "phase3_sites"
_P5 = "phase5_counts"
_P5S = "phase5_sites"
_READ = "codex readings: "


def section(numbers):
    """The section's headings and contents."""
    heading = mb_html.heading_level_2(SECTION[1], {"id": SECTION[0]})
    return [
        heading,
        mb_html.para("Near-Aleppo differs from MAM in three ways:"),
        mb_html.unordered_list(
            [
                "It evaluates away MAM's templates for alternatives and for some marks.",
                "It follows the codex's conventions of representation, as MAM's "
                "introduction and notes describe them.",
                "It takes the readings of the codex that MAM's notes give.",
            ]
        ),
        mb_html.para(
            "Each subsection of this document says what near-Aleppo has where MAM "
            "has something else. The changes are made in the verse's text, in a note's "
            "target, and in every parameter of a ketiv/qere template, and never in a "
            "note's body, which near-Aleppo keeps as MAM has it."
        ),
        mb_html.para(
            [
                link("MAM's templates evaluated away", "reading-json.html#templates"),
                " are listed in the JSON reference.",
            ]
        ),
        *_templates(numbers),
        *_qamats(numbers),
        *_divine_name(numbers),
        *_divine_title(numbers),
        *_elohim(numbers),
        *_revia(numbers),
        *_ole(numbers),
        *_ketiv_qere(numbers),
        *_maqaf(numbers),
        *_hataf(numbers),
        *_stress(numbers),
        *_readings(numbers),
        *_pointed_ketiv(numbers),
        *doc_he_transfer.section(),
        *doc_daniel_sheva.section(),
        *doc_genesis_ketiv.section(),
    ]


def _heading(subsection):
    return mb_html.heading_level_3(subsection[1], {"id": subsection[0]})


def _sites(numbers, section, key):
    return verse_refs(numbers.snap_sites(section, key))


def _sum(numbers, section, keys, what):
    total = sum(numbers.snap_value(section, key) for key in keys)
    return numbers.record(total, f"{section}: the sum of {what}")


def _templates(numbers):
    if _KEPT_LARGE_LETTER_VERSE != ("A5-Deuter", "32", "6"):
        raise AssertionError("the page names Deuteronomy 32:6's kept large letter")
    if numbers.snap_value(_P2, "special letter word kept, large") != 1:
        raise AssertionError("the page names one kept large-letter site")
    special = "מ:אות-מיוחדת-במילה"
    kept = (
        "נוסח",
        "מ:הערה-2",
        "מ:קו״כ-אם-2",
        "כו״ק",
        "קו״כ",
        "מ:כו״ק מיוחד",
        "כתיב ולא קרי",
        "קרי ולא כתיב",
    )
    rows = [
        [
            he_name("מ:קמץ"),
            [
                "Its parameter ",
                he_name("ד"),
                ", as plain text; its parameter ",
                he_name("ס"),
                " goes.",
            ],
        ],
        [
            he_name("מ:דחי"),
            "Its parameter 1, the word with the deḥi alone; parameter 2, with the "
            "deḥi's poetic stress helper, goes.",
        ],
        [
            he_name("מ:צינור"),
            "Its parameter 1, the word with the tsinnor alone; parameter 2, with "
            "the tsinnor's poetic stress helper, goes.",
        ],
        [
            he_name("מ:כפול"),
            [
                "Its parameter ",
                he_name("כפול"),
                ", the passage's two cantillations in one text, as the codex has "
                "them; the two strands, ",
                he_name("א"),
                " and ",
                he_name("ב"),
                ", go.",
            ],
        ],
        [
            he_name("מ:לגרמיה-2"),
            "U+05C0 HEBREW PUNCTUATION PASEQ directly after the word before it, "
            "which a space already follows.",
        ],
        [
            he_name("מ:פסק"),
            "U+05C0 HEBREW PUNCTUATION PASEQ directly after the word before it, and "
            "the space after it that this template alone supplies.",
        ],
        [
            he_name("מ:מקף אפור"),
            "A space between the two words, so they are chanted separately.",
        ],
        [
            he_name(special),
            [
                "The word without its special letter, MAM's parameter 2, at ",
                numbers.snap(_P2, "special letter word flattened"),
                "; the template kept whole for the suspended letters, at ",
                numbers.snap(_P2, "special letter word kept, suspended"),
                ", and for the large he of Deuteronomy 32:6, at ",
                numbers.snap(_P2, "special letter word kept, large"),
                ", the codex having both.",
            ],
        ],
    ]
    return [
        _heading(TEMPLATES),
        mb_html.para(
            "Evaluating away a template replaces its wrapper with the selected text or character. The table shows the selected result or retained template, including the special-letter templates near-Aleppo keeps."
        ),
        table(
            ["MAM's template", "What near-Aleppo has"],
            rows,
            [HEBREW_CELL, None],
        ),
        mb_html.para("The following templates are kept unevaluated:"),
        mb_html.unordered_list([he_name(name) for name in kept]),
        mb_html.para(
            [
                "In ",
                he_name("נוסח"),
                " and ",
                he_name("מ:הערה-2"),
                ", the target is the first parameter. Templates within the target "
                "are evaluated away or kept unevaluated by the same rules as templates "
                "in the verse itself. Notes whose targets remain unchanged keep "
                "their source body in parameter 2. Changed notes store the reviewed "
                "near-Aleppo clause in parameter 2 and the remaining original "
                "clauses in their MAM-note parameter, including templates within them. "
                "Templates evaluated away in the verse remain unevaluated "
                "in those stored source clauses. This preserves MAM's quotations of "
                "readings from other editions. The HTML edition renders those retained "
                "templates when displaying the note.",
            ]
        ),
        mb_html.para(
            "In the ketiv/qere templates in this list, templates within every "
            "parameter follow the verse's rules for evaluation or retention, including parameters "
            "for readings that near-Aleppo does not select."
        ),
        *doc_template_examples.examples(),
        mb_html.para(
            [
                "A ketiv/qere template's parameters other than the one near-Aleppo's "
                "text follows use the same rules. In those parameters, near-Aleppo evaluates away ",
                numbers.snap(_P2, "מ:קמץ (unselected parameter)"),
                " ",
                he_name("מ:קמץ"),
                ", ",
                numbers.snap(_P2, "מ:דחי (unselected parameter)"),
                " ",
                he_name("מ:דחי"),
                ", ",
                numbers.snap(_P2, "מ:לגרמיה-2 (unselected parameter)"),
                " ",
                he_name("מ:לגרמיה-2"),
                ", and ",
                numbers.snap(
                    _P2, "special letter word flattened (unselected parameter)"
                ),
                " special-letter template besides. So ",
                *_listed([he_name(name) for name in TEMPLATES_ABSENT_FROM_DATASET]),
                " occur nowhere in near-Aleppo's text, in no column, parameter, or "
                "note body; only the copies of MAM's target have them.",
            ]
        ),
        mb_html.para(
            [
                "Where MAM has a legarmeh, ",
                he_name("מ:לגרמיה-2"),
                ", or a narrow-sense paseq, ",
                he_name("מ:פסק"),
                ", near-Aleppo writes the same character, U+05C0, so its text does "
                "not tell the two apart. The note bodies, which near-Aleppo keeps "
                "verbatim, still have both templates.",
            ]
        ),
    ]


def _qamats(numbers):
    return [
        _heading(QAMATS),
        mb_html.para(
            [
                "The codex has no separate sign for the qamats qatan. Where MAM has "
                "HEBREW POINT QAMATS QATAN, near-Aleppo has HEBREW POINT QAMATS, at ",
                numbers.snap(
                    _P3, "HEBREW POINT QAMATS QATAN changed to HEBREW POINT QAMATS"
                ),
                " places in its text and ",
                numbers.snap(
                    _P3,
                    "HEBREW POINT QAMATS QATAN changed to HEBREW POINT QAMATS "
                    "(unselected parameter)",
                ),
                " more in a ketiv/qere template's other parameters. So HEBREW POINT "
                "QAMATS in near-Aleppo is, in Ben Denckla's words, “an ambiguous "
                "qamats, not a qamats gadol”. The note bodies and the copies of MAM's "
                "target keep MAM's qamats qatan.",
            ]
        ),
        mb_html.para(
            [
                "The ",
                link("qamats template example", "reading-json.html#templates"),
                " shows both Unicode qamats characters and the final near-Aleppo form.",
            ]
        ),
    ]


def _divine_name(numbers):
    return [
        _heading(DIVINE_NAME),
        mb_html.para(
            [
                "Where the divine name is read Adonai, MAM has a holam on its first "
                "he, and MAM's introduction says that the codex does not write it "
                "there except in a few places, which MAM's notes record. Near-Aleppo "
                "has no holam there, at ",
                numbers.snap(_P3, "Adonai reading: holam on the first he stripped"),
                " words, and keeps it at the ",
                numbers.snap(
                    _P3, "Adonai reading: holam kept where a note records the codex's"
                ),
                " whose notes record the codex's: ",
                _sites(
                    numbers,
                    _P3S,
                    "Adonai reading: holam kept where a note records the codex's",
                ),
                ". Where the divine name is read Elohim, the codex has the holam, and "
                "near-Aleppo has it as MAM does.",
            ]
        ),
        *doc_policy_examples.comparison("divine-name"),
    ]


def _divine_title(numbers):
    return [
        _heading(DIVINE_TITLE),
        mb_html.para(
            [
                "Where a word ending in the letters ",
                he_name(_ADONAI_LETTERS),
                " is the divine title, with a qamats on its nun, MAM has a holam on "
                "its dalet, which MAM's introduction says the codex writes only in "
                "isolated places. Near-Aleppo has no holam there, at ",
                numbers.snap(_P3, "divine title: holam on the dalet stripped"),
                " words, and keeps it at ",
                _sites(
                    numbers,
                    _P3S,
                    "divine title: holam kept where a note records the codex's",
                ),
                ", whose note records the codex's. The other ",
                numbers.snap(
                    _P3, "atom ending in אדני without a qamats on the nun, unchanged"
                ),
                " words ending in those letters, which are not the title, are as MAM "
                "has them.",
            ]
        ),
        *doc_policy_examples.comparison("divine-title"),
    ]


def _elohim(numbers):
    return [
        _heading(ELOHIM),
        mb_html.para(
            [
                "Where the divine name is read Elohim, MAM has a hataf segol on its "
                "yod, and near-Aleppo has a sheva there, at ",
                numbers.snap(
                    _P3, "Elohim reading: sheva for the hataf segol on the yod"
                ),
                " words. At ",
                _sites(numbers, _P3S, "Elohim reading: yod with no vowel, unchanged"),
                " the yod has no vowel, and near-Aleppo has it as MAM does.",
            ]
        ),
        *doc_policy_examples.comparison("elohim"),
    ]


def _revia(numbers):
    numbers.require_sites(
        _P3S,
        ("revia mugrash: revia kept where chapter 5 records the codex's",),
        (("D2-Proverbs", "19", "26"),),
    )
    numbers.require_sites(
        "flag_sites", ("named doubtful agreeing clause",), ("D2-Proverbs|19|26",)
    )
    return [
        _heading(REVIA),
        mb_html.para(
            [
                "Where MAM has a revia and a geresh muqdam on one letter, the revia "
                "mugrash, near-Aleppo has the geresh muqdam alone, at ",
                numbers.snap(
                    _P3, "revia mugrash: revia removed from the geresh muqdam's letter"
                ),
                " sites. Chapter 5 of MAM's introduction lists every such site with "
                "the codex's reading. Near-Aleppo keeps the revia at the ",
                numbers.snap(
                    _P3, "revia mugrash: revia kept where chapter 5 records the codex's"
                ),
                " sites where chapter 5, or the note on the word, records it in the "
                "codex: ",
                _sites(
                    numbers,
                    _P3S,
                    "revia mugrash: revia kept where chapter 5 records the codex's",
                ),
                ". The record at Proverbs 19:26 is doubt-marked, and the site is "
                "flagged. At ",
                _sites(
                    numbers,
                    _P3S,
                    "revia mugrash: geresh muqdam moved to the compound's first atom",
                ),
                " it has the two marks split across a maqaf compound, as the codex "
                "has them: the geresh muqdam on the compound's first word and the "
                "revia where MAM has it. Where the site is in a note's target, the "
                "note's form of the codex's word agrees with near-Aleppo's, at all ",
                numbers.snap(
                    _P3,
                    "revia mugrash: removal agreeing with a codex form its note quotes",
                ),
                " such sites.",
            ]
        ),
        *doc_policy_examples.comparison("revia"),
    ]


def _ole(numbers):
    return [
        _heading(OLE),
        mb_html.para(
            [
                "Where MAM has an ole and a yored on one letter, near-Aleppo has the "
                "yored alone; the yored's Unicode name is HEBREW ACCENT MERKHA. "
                "Chapter 2 of MAM's introduction says that the manuscripts have the "
                "yored alone where its syllable begins its word and the word before "
                "it is stressed on its last syllable or has a disjunctive accent, as "
                "Yeivin does (",
                itm(),
                " §360). Chapter 5 lists the verses where MAM has both marks on one "
                "letter, saying that the codex has no ole in any of them: ",
                _sites(numbers, _P3S, "ole on the yored's letter: ole removed"),
                ". Where the letter is in a note's target, near-Aleppo's word is the "
                "form the note's clauses citing the codex give, at all ",
                numbers.snap(
                    _P3,
                    "ole on the yored's letter: removal agreeing with the codex form its note quotes",
                ),
                " such letters. The other ",
                numbers.snap(_P3, "ole on a letter without the yored, unchanged"),
                " oles, each on a letter without a yored, are as MAM has them.",
            ]
        ),
        *doc_policy_examples.comparison("ole"),
    ]


_SPELLING_NOTE_SITES = (
    ("A5-Deuter", "32", "13"),
    ("B1-Joshua", "3", "4"),
    ("C3-Ezekiel", "40", "24"),
    ("CA-The-12-Minor-Prophets צפניה", "2", "9"),
)


def _ketiv_qere(numbers):
    form = "ketiv/qere apparatus: template replaced by the codex form its note quotes"
    ketiv = "ketiv/qere apparatus: template replaced by its pointed ketiv"
    qere = (
        "ketiv/qere apparatus: template replaced by its pointed qere, the spelling "
        "its note's prose gives the codex"
    )
    transplant = "ketiv/qere apparatus: template replaced by MAM's ketiv pointed by the transplant"
    kept = "ketiv/qere apparatus: template kept where the codex form is doubt-marked"
    numbers.require_sites(_P3S, (form, ketiv, qere, transplant), _SPELLING_NOTE_SITES)
    return [
        _heading(KETIV_QERE),
        mb_html.para(
            "The ketiv/qere apparatus is the one part of the masorah near-Aleppo "
            "represents: a ketiv/qere template stands where the codex has a qere "
            "note. So where MAM's note on a ketiv/qere word says that the codex has "
            "no qere note there, near-Aleppo has plain text in place of the template. "
            "It reads a note in the same way where the note gives the codex's masorah "
            "note on the word and that note is not a qere note, as at Deuteronomy "
            "32:13, Joshua 3:4, and Zephaniah 2:9, and at the second site of Ezekiel "
            "40:24."
        ),
        mb_html.para(
            [
                "The plain text is the form of the codex's word that the note quotes, "
                "at ",
                numbers.snap(_P3, form),
                " sites (",
                _sites(numbers, _P3S, form),
                "); MAM's pointed ketiv, parameter 1 of a ",
                he_name("מ:קו״כ-אם-2"),
                ", at ",
                numbers.snap(_P3, ketiv),
                " (",
                _sites(numbers, _P3S, ketiv),
                "); MAM's pointed qere, the spelling that the note's prose gives the "
                "codex, at ",
                _sites(numbers, _P3S, qere),
                "; or MAM's ketiv, each of whose letters has the marks that the same "
                "letter has in the qere, at ",
                numbers.snap(_P3, transplant),
                " (",
                _sites(numbers, _P3S, transplant),
                "). At ",
                _sites(numbers, _P3S, kept),
                " the note's form of the codex's word is doubt-marked, so near-Aleppo "
                "keeps the template there, and flags the site.",
            ]
        ),
        *doc_policy_examples.apparatus_example(),
    ]


def _maqaf(numbers):
    added = "maqaf: maqafs added"
    split = "maqaf: clause form has a maqaf inside one target atom"
    space = "maqaf: clause form has a space where the target had a maqaf"
    return [
        _heading(MAQAF),
        mb_html.para(
            [
                "Where a clause of a note citing the codex gives it a form that "
                "differs from MAM's target only in a maqaf, near-Aleppo has the "
                "form: ",
                _sum(
                    numbers,
                    _P3,
                    (
                        "maqaf: undoubted clauses applied",
                        "maqaf: bang-marked clauses applied",
                    ),
                    "the maqaf clauses applied",
                ),
                " clauses, ",
                numbers.snap(_P3, "maqaf: bang-marked clauses applied"),
                " of them marked in the note as a manifest error in the codex, and "
                "flagged. Near-Aleppo has a maqaf where MAM has none at ",
                numbers.snap(_P3, added),
                " sites, ",
                numbers.snap(_P3, split),
                " of them inside one of MAM's words: ",
                _sites(numbers, _P3S, added),
                ". It has a space where MAM has a maqaf at ",
                numbers.snap(_P3, space),
                ": ",
                _sites(numbers, _P3S, space),
                ". A doubt-marked clause of the kind is flagged and not taken, as "
                "every doubtful reading is.",
            ]
        ),
        *doc_policy_examples.comparison("maqaf"),
        mb_html.para(
            "This is the note's first quoted Aleppo form, with the merkha retained, "
            "under the recorded choice for Job 23:5."
        ),
    ]


def _hataf(numbers):
    hiriq = "hataf on a non-guttural: varika replaced by a hiriq, the sheva kept"
    return [
        _heading(HATAF),
        mb_html.para(
            [
                "Where the manuscripts have a hataf on a letter that is not a "
                "guttural, MAM has a sheva with a varika, U+FB1E HEBREW POINT "
                "JUDEO-SPANISH VARIKA, and gives the hataf's form in its note on the "
                "word. Near-Aleppo has the hataf, reading each vowel from the note: a "
                "hataf patah at ",
                numbers.snap(
                    _P3,
                    "hataf on a non-guttural: sheva and varika replaced by a hataf patah",
                ),
                " letters and a hataf qamats at ",
                numbers.snap(
                    _P3,
                    "hataf on a non-guttural: sheva and varika replaced by a hataf qamats",
                ),
                ". At the ",
                numbers.snap(_P3, hiriq),
                " letters where MAM's notes give the codex a hataf hiriq, ",
                _sites(numbers, _P3S, hiriq),
                ", near-Aleppo has the sheva with a hiriq, as each note writes the "
                "codex's form. At all ",
                numbers.snap(
                    _P3,
                    "hataf on a non-guttural: restoration agreeing with a form its note quotes",
                ),
                " letters near-Aleppo's letter agrees with a form the note quotes.",
            ]
        ),
        *doc_policy_examples.comparison("hataf"),
        *doc_policy_examples.comparison("hataf-hiriq"),
        mb_html.para(
            [
                "Near-Aleppo has the hataf at every varika of MAM's, whichever "
                "sources the note cites. Of the ",
                numbers.fig("varika_notes"),
                " notes on a varika, ",
                numbers.fig("varika_notes_without_codex_siglum"),
                " quote the hataf's form under no siglum beginning with ",
                he_name("א"),
                ", so that there the hataf rests on the convention and on other "
                "manuscripts rather than on a reading of the codex.",
            ]
        ),
    ]


def _stress(numbers):
    numbers.require_sites(
        _P3S,
        (
            "stress helpers: geresh or gershayim removed with a telisha gedolah's stress helper",
        ),
        (("A3-Levit", "10", "4"),),
    )
    kept_codex = "stress helpers: kept by a note citing the codex"
    kept_l = "stress helpers: kept by a note citing ל"
    kept_keys = [
        f"stress helpers: {accent}'s stress helper kept by a note whose agreeing "
        f"clause {cites} for the doubling{rest}"
        for accent in (
            "pashta",
            "segolta",
            "telisha qetanah",
            "telisha gedolah",
            "zarqa",
        )
        for cites, rest in (
            ("cites the codex", ""),
            ("cites ל", ", no clause citing the codex"),
        )
    ]
    stripped = [
        ("segolta", "segolta"),
        ("telisha qetanah", "telisha qetanah"),
        ("telisha gedolah", "telisha gedolah"),
        ("zarqa", "zarqa"),
    ]
    stripped_text = []
    for index, (label, accent) in enumerate(stripped):
        if index:
            stripped_text.append(", and " if index == len(stripped) - 1 else ", ")
        stripped_text += [
            numbers.snap(_P3, f"stress helpers: {accent}'s stress helper stripped"),
            f" words with the {label}" if index == 0 else f" with the {label}",
        ]
    return [
        _heading(STRESS),
        mb_html.para(
            [
                "A stress helper is a second copy of an accent that stands at an edge "
                "of its chanted word, put on the first letter of the stressed "
                "syllable. The codex writes the pashta's stress helper except where "
                "no letter stands between the stressed letter and the word's last "
                "letter (Yeivin, ",
                itm(),
                " §239), and near-Aleppo has that convention, where the codex is lost "
                "too. Where MAM has the pashta's stress helper on a word's "
                "second-to-last letter, near-Aleppo has the pashta alone, at ",
                numbers.snap(_P3, "stress helpers: pashta's stress helper stripped"),
                " words, and it keeps the other ",
                numbers.snap(
                    _P3,
                    "stress helpers: pashta's stress helper kept, a letter standing between",
                ),
                ", a mater lectionis counting as a letter between. Where MAM has the "
                "stress helper of another accent, near-Aleppo has the accent alone: at ",
                *stripped_text,
                ". Every stress helper this policy strips is in a prose verse. "
                "In a poetic verse the characters of a zarqa and its helper are "
                "the tsinnor and the tsinnorit, two accents, which near-Aleppo keeps. "
                "The poetic stress helpers of the deḥi and the tsinnor go with MAM's "
                "templates for them.",
            ]
        ),
        mb_html.para(
            [
                "Near-Aleppo keeps the ",
                _sum(numbers, _P3, kept_keys, "the stress helpers kept by notes"),
                " stress helpers that MAM's notes record in the codex, at ",
                _sites(numbers, _P3S, kept_codex),
                ", or, where the codex is lost, in the Leningrad Codex, at ",
                _sites(numbers, _P3S, kept_l),
                ". At Leviticus 10:4 near-Aleppo follows the note's testimony to the "
                "codex's lost part, cited as ",
                he_name("א(ס)"),
                ": the telisha gedolah on the qof and the gershayim on the bet.",
            ]
        ),
        mb_html.para(
            [
                "The ",
                link("Genesis 2:7 example", "index.html#what-the-dataset-is"),
                " shows a removed telishah qetannah stress helper.",
            ]
        ),
    ]


def _readings(numbers):
    rows = [
        (
            "Already in place, after the conventions above",
            (
                "apply-candidate already in place",
                "apply-candidate in place, its form lacking the paseq glyph that ends the target",
            ),
        ),
        (
            "In place in a ketiv/qere template's qere, or through the ketiv/qere "
            "apparatus",
            (
                "ketiv/qere plane reading in place in a qere parameter",
                "ketiv/qere plane reading in place through phase 3's ketiv/qere apparatus",
            ),
        ),
        (
            "Taken, in place of MAM's target or of some of its words, or in the "
            "ketiv/qere template that is the target",
            (
                "applied, the form replacing the whole of a plain target",
                "applied, the form replacing named atoms of a plain target",
                "applied, the form written into the selected parameter of the one kept "
                "template that is the target",
            ),
        ),
        (
            ["Taken as the pointed ketiv, in ", he_name(POINTED_KETIV_PARAMETER)],
            (
                "pointed ketiv written as the form stands",
                "pointed ketiv written with a named adjustment",
            ),
        ),
        (
            "Not taken, being doubt-marked, and flagged",
            ("do-not-apply (doubt-siglum)", "do-not-apply (doubt-form)"),
        ),
        (
            "Not taken, the note's prose outweighing it, and flagged",
            ("not applied, and flagged",),
        ),
        (
            "Left as MAM has it, being a description in prose rather than a form",
            ("do-not-apply (prose-description)",),
        ),
        (
            "Not yet read or not yet taken",
            (
                "ketiv/qere plane reading pending by name",
                "ketiv/qere plane reading at a one-sided template, left for later work",
                "pending, the form stopping at the codex's space for a qere without ketiv",
                "policy-pending (candidate-form-punctuation)",
                "policy-pending (candidate-form-count-0)",
            ),
        ),
    ]
    total = numbers.snap_value(_P5, _READ + "direct differing clauses")
    parts = sum(
        numbers.snap_value(_P5, _READ + key) for _, keys in rows for key in keys
    )
    if parts != total:
        raise AssertionError(f"the outcomes add up to {parts}, not {total}")
    table_rows = [
        [
            label,
            _sum(
                numbers,
                _P5,
                tuple(_READ + key for key in keys),
                "the clauses of one outcome",
            ),
        ]
        for label, keys in rows
    ]
    return [
        _heading(READINGS),
        mb_html.para(
            [
                "Where a clause of a ",
                he_name("נוסח"),
                " note cites the codex for a reading that differs from MAM's text, "
                "near-Aleppo takes the reading, if the clause is undoubted and quotes "
                "one pointed form. The clause cites the codex by a siglum for its "
                "text or for testimony to its lost parts. MAM's notes have ",
                numbers.snap(_P5, _READ + "direct differing clauses"),
                " such clauses, in ",
                numbers.snap(_P5, _READ + "verses with a direct differing clause"),
                " verses, and the table gives what near-Aleppo has of each.",
            ]
        ),
        table(
            ["What near-Aleppo has of the reading", "Clauses"],
            table_rows,
            [None, NUMBER_CELL],
        ),
        mb_html.para(
            [
                "Of the readings near-Aleppo has, ",
                numbers.snap(
                    "flag_counts", "qualification 3: differing clauses already applied"
                ),
                " are marked in their notes as manifest errors in the codex, and each "
                "is flagged. Where the codex is lost, near-Aleppo also has the "
                "readings of the clauses naming the codex's method, ",
                he_name("שיטת-א"),
                ": ",
                numbers.snap(_P5, _READ + "differing clauses whose head names שיטת-א"),
                " differing clauses, of which ",
                numbers.snap(_P5, _READ + "שיטת-א reading already in place"),
                " are in place already, the one at ",
                _sites(
                    numbers,
                    _P5S,
                    _READ + "שיטת-א reading applied, the whole of a plain target",
                ),
                " is taken, and the one at ",
                _sites(numbers, _P5S, _READ + "שיטת-א reading not applied"),
                " gives way to the testimony the stress helpers follow there.",
            ]
        ),
        mb_html.para(
            [
                "The ",
                link("Isaiah 27:5 example", "index.html#what-the-dataset-is"),
                " compares MAM's target with the Aleppo form quoted in its note.",
            ]
        ),
    ]


_ADJUSTMENTS = (
    ('BA-Samuel שמ"ב', "5", "2"),
    ('BA-Samuel שמ"ב', "21", "12"),
    ("C1-Isaiah", "36", "12"),
    ("C1-Isaiah", "44", "24"),
    ("D2-Proverbs", "3", "30"),
)


def _pointed_ketiv(numbers):
    adjusted = _READ + "pointed ketiv written with a named adjustment"
    if sorted(map(verse_key, numbers.snap_sites(_P5S, adjusted))) != sorted(
        _ADJUSTMENTS
    ):
        raise AssertionError("the page names the adjusted pointed ketivs' sites")
    return [
        _heading(POINTED_KETIV),
        mb_html.para(
            [
                "Where MAM's notes give the pointed ketiv that the codex has at a "
                "ketiv/qere template, under the siglum ",
                he_name("א-כתיב"),
                " or under a plain ",
                he_name("א"),
                " with the ketiv's letters, near-Aleppo writes it in the parameter ",
                he_name(POINTED_KETIV_PARAMETER),
                ", and its text follows that parameter: at ",
                numbers.fig("note_pointed_ketiv_templates"),
                " templates. At ",
                numbers.snap(_P5, _READ + "pointed ketiv written as the form stands"),
                " the parameter is the note's form as it stands, and at ",
                numbers.snap(_P5, adjusted),
                " it has an adjustment: without the note's masorah circles, at 2 "
                "Samuel 5:2 and 21:12; with the maqaf of the note's form where MAM's "
                "ketiv has a space, at Isaiah 44:24, as the note says the two words "
                "are read together; with the marks that the note writes on bracketed "
                "alefs written as the near-Aleppo dataset's template ",
                he_name(MARKS_WITHOUT_LETTER),
                ", at Isaiah 36:12; and at Proverbs 3:30, with a space where MAM has "
                "a maqaf before the template, as the note's form has it. Of the "
                "forms, ",
                numbers.snap(
                    _P5, _READ + "pointed ketiv ending in the qere's trailing maqaf"
                ),
                " end in the maqaf that follows MAM's qere.",
            ]
        ),
        mb_html.para(
            [
                "An approved frozen source-only algorithm supplies a further ",
                numbers.fig("inferred_pointed_ketiv_templates"),
                " pointed-ketiv parameters from MAM's ketiv and pointed qere "
                "after the representation policies. Each accepted prediction "
                "has one surviving canonical candidate and no unresolved "
                "ownership node. Other transfer and source-accounting warnings "
                "are retained in a separate source archive; singleton selection "
                "is categorical, not a probability or a guarantee of correctness. "
                "MAM-note pointings take priority. The frozen import adds no "
                "source attribution or diagnostic metadata to a template.",
            ]
        ),
        mb_html.para(
            [
                "Individual editorial adjudication supplies a further ",
                numbers.fig("editorial_pointed_ketiv_templates"),
                " pointed-ketiv parameters, at Genesis 43:28, Ezekiel 42:9, "
                "and Daniel 5:7, 5:21, and 5:29. "
                "The ",
                link("mobile he cases", "ketiv-qere-mobile-he.html"),
                " explain the unattached patah in Ezekiel; the ",
                link("Genesis 43:28 case", "ketiv-qere-genesis-43-28.html"),
                " and ",
                link("Daniel cases", "ketiv-qere-daniel.html"),
                " explain inferred readings where Aleppo is not extant. "
                "These decisions are recorded separately from the frozen algorithmic predictions.",
            ]
        ),
        mb_html.para(
            [
                "A sealed reviewed portable import supplies a further ",
                numbers.fig("reviewed_pointed_ketiv_templates"),
                " pointed-ketiv parameters: case-specific choices and source-supported "
                "agreements admitted under the approved plan only after checking "
                "current targets, notes, prior pointings, written letters and atom "
                "boundaries. It preserves current qeres and edition punctuation, "
                "and includes only the sealed pointings and target guards. "
                "All retained paired ketiv/qere templates now have an adopted "
                "pointing. Prior note-derived, frozen and individual "
                "pointings retain priority.",
            ]
        ),
    ]


def _listed(items):
    out = []
    for index, item in enumerate(items):
        if index:
            if index == len(items) - 1:
                out.append(", and " if len(items) > 2 else " and ")
            else:
                out.append(", ")
        out.append(item)
    return out
