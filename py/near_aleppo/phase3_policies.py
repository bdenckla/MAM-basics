"""Phase 3 of near-aleppo: the representation policies, in the E column.

The public build guide is ``doc/near-aleppo-build.md``. The policies run at
every verse, whether or not the codex survives there. This module implements
ten representation policies: the qamats size, the YHVH-Elohim
vowel, the divine-name holam, the Adonai holam, the revia mugrash, the ole on the
yored's letter, the ketiv/qere apparatus, the hataf on a non-guttural, the
stress helpers, and the maqaf.

The ketiv/qere apparatus, alone of these policies, replaces a template. At 16 of
the 17 verses where MAM's note on an atom says the codex has no qere note, it
replaces the ketiv/qere template in the note's target by plain text, and it does
the same at four sites where the note gives the codex's masorah note on the atom
and that note is not a qere note. The four are explicitly named policy choices,
as the apparatus's tables below explain. The apparatus runs first, before the note's
target is walked, so the other policies run over the text it inserts.

A policy changes the text phase 2 leaves in three places: the verse's text outside
templates, the selected parameter of a kept note template, and every parameter of
a kept ketiv/qere template, selected or not. This matches phase 2's handling of
templates in those parameters. What a policy finds
in an unselected parameter is counted apart, so that the census's figures, which
count only the selected parameters, are asserted as the census states them. Two
kinds of text stay as phase 2 left them: a note body, which rule 2 keeps verbatim,
and the parameters of a layout or separator template, which hold no Scripture.

Phase 3 walks the templates phase 2 keeps by phase 2's rule table, asking its
selected_keys which parameters are selected, so the two phases cannot disagree
about which parameter is selected, and a template that table does not keep raises.
Phase 3 runs before phase 5 adds the pointed ketiv MAM's notes give, so it selects
the pointed qere of every ordinary ketiv/qere template, and its counts of selected
and unselected parameters are those of MAM's selection.

A special-letter word that phase 2 keeps has the same text in parameters 1 and 2,
once with the special letter's template and once without, so a policy's target
inside one raises rather than leaving the two parameters out of step.

The policies that look at letters divide a string into atoms and letters as the
census's ``clusters()`` does, so that they find the populations the census counts:
an atom ends at a space or a maqaf, each mark belongs to the letter before it, and
any other character is passed over.

Each population is re-derived on every build and a mismatch raises. A note's
quotation of the codex is independent of the list or the criterion a policy
follows, so the removals of the revia mugrash and of the ole on the yored's letter
are also checked against the notes whose targets hold them, and the ketiv/qere
apparatus's transplant is checked against the codex forms its notes quote and
against MAM's pointed ketiv, and the pointed qere it takes at one site against the
form the note there gives the codex in prose. The hataf on a non-guttural reads
each vowel from the note whose target holds the varika, asserts that MAM-basics'
inference gives the same vowel, and checks each restored letter against a form the
note quotes. Each stress helper in a note's target, stripped or kept, is checked
against the codex forms the note quotes.

The maqaf policy, the hataf on a non-guttural and the stress-helper policy also
read a note before the note's target is walked, after the ketiv/qere apparatus.
The maqaf policy puts the note's codex form in the target. The hataf policy decides
the vowels of the target's varikas, in order, and the walk applies them in the
order it meets the varikas. The stress-helper policy decides whether the target
keeps its stress helpers.
"""

from collections import Counter
from collections import defaultdict
import re
import unicodedata

from mb_cmn import template_names
from near_aleppo import phase2_templates as phase2

CGJ = "\N{COMBINING GRAPHEME JOINER}"
DAGESH = "\N{HEBREW POINT DAGESH OR MAPIQ}"
GERESH = "\N{HEBREW ACCENT GERESH}"
GERESH_MUQDAM = "\N{HEBREW ACCENT GERESH MUQDAM}"
GERSHAYIM = "\N{HEBREW ACCENT GERSHAYIM}"
HATAF_PATAH = "\N{HEBREW POINT HATAF PATAH}"
HATAF_QAMATS = "\N{HEBREW POINT HATAF QAMATS}"
HATAF_SEGOL = "\N{HEBREW POINT HATAF SEGOL}"
HIRIQ = "\N{HEBREW POINT HIRIQ}"
HOLAM = "\N{HEBREW POINT HOLAM}"
MAQAF = "\N{HEBREW PUNCTUATION MAQAF}"
MASORA_CIRCLE = "\N{HEBREW MARK MASORA CIRCLE}"
OLE = "\N{HEBREW ACCENT OLE}"
PASEQ = "\N{HEBREW PUNCTUATION PASEQ}"
PASHTA = "\N{HEBREW ACCENT PASHTA}"
QAMATS = "\N{HEBREW POINT QAMATS}"
QAMATS_QATAN = "\N{HEBREW POINT QAMATS QATAN}"
REVIA = "\N{HEBREW ACCENT REVIA}"
# The segolta, whose Unicode name is HEBREW ACCENT SEGOL.
SEGOLTA = "\N{HEBREW ACCENT SEGOL}"
SHEVA = "\N{HEBREW POINT SHEVA}"
TELISHA_GEDOLA = "\N{HEBREW ACCENT TELISHA GEDOLA}"
TELISHA_QETANA = "\N{HEBREW ACCENT TELISHA QETANA}"
# Unicode ZARQA and Unicode ZINOR, whose Unicode names disagree with the Masoretic
# ones. In a prose verse MAM has the zarqa as Unicode ZINOR and the zarqa's stress
# helper as Unicode ZARQA; in a poetic verse Unicode ZINOR is the tsinnor and
# Unicode ZARQA the tsinnorit.
UNICODE_ZARQA = "\N{HEBREW ACCENT ZARQA}"
UNICODE_ZINOR = "\N{HEBREW ACCENT ZINOR}"
VARIKA = "\N{HEBREW POINT JUDEO-SPANISH VARIKA}"
# The yored, whose Unicode name is HEBREW ACCENT MERKHA.
YORED = "\N{HEBREW ACCENT MERKHA}"

_LETTERS = frozenset(chr(c) for c in range(0x05D0, 0x05EB))
# As in the census: U+0591 to U+05C7, the CGJ and the varika each belong to the
# letter before them.
_MARKS = frozenset(chr(c) for c in range(0x0591, 0x05C8)) | {CGJ, VARIKA}
# The vowel points, sheva to qubuts, and the qamats qatan.
_VOWELS = frozenset(chr(c) for c in range(0x05B0, 0x05BC)) | {QAMATS_QATAN}

_DIVINE_NAME_LETTERS = "יהוה"
_ADONAI_LETTERS = "אדני"
_ADONAI = "Adonai"
_ELOHIM = "Elohim"

# The note template whose body can record what the codex has at its target.
_NOTE = "נוסח"
# How MAM's note opens where it records the codex's holam in the divine name:
# "=א (in the manuscript a holam dot was written in the divine name)".
_CODEX_DIVINE_NAME_HOLAM_NOTE = '=א (בכתב־היד נכתבה נקודת חולם בשם הוי"ה)'
# How it opens where it records the codex's holam in the divine title:
# "=א (a holam dot in the manuscript)".
_CODEX_TITLE_HOLAM_NOTE = "=א (נקודת חולם בכתב־היד)"

# The revia mugrash. Where an atom is stressed on its first syllable, MAM puts the
# revia on the geresh muqdam's letter for the reader, and the codex usually has the
# geresh muqdam alone there. Chapter 5 of MAM's
# introduction, section "רביע מוגרש", lists all 260 letters with both marks, giving
# the codex's reading at each (in/mam-ws-intro/ch5.mediawiki). The revia is removed at
# every one of them except in the verses of the two tables below, and each verse a
# table names has exactly one such letter.
#
# The revia is kept where chapter 5's entry says the codex has it, and at Proverbs
# 19:26, where the entry's siglum is doubt-marked (א?). At Psalms 105:2 the note on
# the atom said the codex lacks the revia, against chapter 5's entry. Ben read the
# codex on 2026-09-15 as having it and changed the note on Wikisource that day to
# say so, and he also read the revia in the codex at Psalms 27:12, whose atom had
# no note, and added the same note there (MAM-basics#282). Both changes reached
# MAM-parsed-plus in the committed refresh of 2026-09-17. Neither changes this
# table, which names verses.
_REVIA_KEPT_VERSES = (
    ("D1-Psalms", "7", "1"),
    ("D1-Psalms", "25", "21"),
    ("D1-Psalms", "27", "12"),
    ("D1-Psalms", "35", "14"),
    ("D1-Psalms", "77", "17"),
    ("D1-Psalms", "105", "2"),
    ("D2-Proverbs", "19", "26"),
)
# The geresh muqdam moves at Job 19:16, where chapter 5's entry (א!) and the note
# both give the codex the geresh muqdam on the bet of the compound's first atom and
# the revia on the pe of its second, while MAM has both marks on the pe.
_GERESH_MUQDAM_MOVED_VERSES = (("D3-Job", "19", "16"),)
# That first atom, במו, as (letter, marks), the marks in MAM's order. The geresh
# muqdam goes on the bet after its dagesh and sheva, which is where the note's form
# has it.
_BEMO = [("ב", [DAGESH, SHEVA]), ("מ", []), ("ו", [HOLAM])]
# Neither table names a verse of Psalms 15:1-25:1, where the codex is lost and
# chapter 5 gives the Leningrad Codex's reading instead, with the revia at nine of
# the ten letters. The policy removes the revia at those nine: each note has a
# שיטת-א clause omitting it, and the dataset admits שיטת-א where the codex is lost.

# The check of the revia removals against the notes, and the ketiv/qere apparatus,
# read a note body's clauses, which ש templates separate. In the check of the
# removals, a clause citing one of these sigla quotes the codex.
_CLAUSE_SEPARATOR = "ש"
_CODEX_SIGLA = frozenset({"א", "א-קרי", "שיטת-א"})
# "Like": in a clause, the sigla after this word have the clause's form too.
_LIKE = "כמו"
# The committed MAM refresh of 2026-09-17 includes the geresh muqdam in
# Psalms 73:6's quoted form. No note now needs the former exception; the
# population snapshot pins its count and site list at zero and empty.
_NOTE_FORM_WITHOUT_GERESH_MUQDAM_VERSES = ()

# The ole on the yored's letter. Chapter 5 of MAM's introduction,
# section "עולה ויורד", part א, lists the 13 verses where MAM has the ole and the
# yored on one letter, with the codex's form at each
# (in/mam-ws-intro/ch5.mediawiki). The check of the removals against the notes
# reads a clause as citing the codex where a siglum of its head, less any "!" or
# "?", is this one.
_OLE_CODEX_SIGLUM = "א"
# In such a clause the quoted target is followed by the clause's end, a space, a "("
# or a ">".
_OLE_AFTER_QUOTED_TARGET = ("", " ", "(", ">")

# The ketiv/qere apparatus is the one part of the masorah the dataset retains.
# A ketiv/qere template is replaced by plain text where MAM's note says the codex
# has no qere note: 16 of the 17 verses, with Jeremiah 33:26 kept because its form
# is doubt-marked.
#
# Four named policy choices also treat a masorah note that is not a qere note as
# grounds for replacing the template: Deuteronomy 32:13, Joshua 3:4,
# Ezekiel 40:24's second site and Zephaniah 2:9. These are interpretive choices;
# retaining the apparatus at these sites would also be a possible policy. The
# tables record the chosen text explicitly, and the build checks that each note
# still supplies the evidence its site's disposition assumes.
#
# The tables name 21 sites at 20 verses, two at Ezekiel 40:24. Each site's note
# target has the template as a direct element.
#
# At the form-from-note sites, one clause headed א or א-כתיב quotes the codex's
# target. The replacement is that form less the target's text before and after
# the template, grouped by family. At Deuteronomy 32:13 the clause headed א also
# quotes the masorah note מ"ק-א=<ג' מל'>, three times written plene.
_KQ_FORM_FROM_NOTE_VERSES = (
    (("A5-Deuter", "32", "13"), "קו״כ"),
    (('BA-Samuel שמ"א', "10", "7"), "כו״ק"),
    (("C1-Isaiah", "18", "4"), "כו״ק"),
    (("C1-Isaiah", "44", "17"), "כו״ק"),
    (("C1-Isaiah", "58", "14"), "קו״כ"),
    (("C3-Ezekiel", "21", "28"), "כו״ק"),
    (("C3-Ezekiel", "24", "2"), "כו״ק"),
    (("C3-Ezekiel", "44", "3"), "כו״ק"),
    (("CA-The-12-Minor-Prophets נחום", "1", "3"), "כו״ק"),
    (("CA-The-12-Minor-Prophets נחום", "2", "1"), "כו״ק"),
    (("D1-Psalms", "89", "29"), "כו״ק"),
    (('FC-Chronicles דה"ב', "25", "17"), "כו״ק"),
    (('FC-Chronicles דה"ב', "34", "22"), "קו״כ"),
)
# The form has the ketiv's letters at each of those verses but this one, where the
# note's א clause gives the codex the qere's letters and denies an explicit qere
# note.
_KQ_FORM_WITH_QERE_LETTERS_VERSES = (("C3-Ezekiel", "24", "2"),)
# At these four the template is a מ:קו״כ-אם-2, whose parameter 1 is already the
# pointed ketiv. The note quotes no codex form, so parameter 1 replaces the template.
# At Ezekiel 40:24's first site, 40:25 and 40:26 the note denies a qere note in prose.
# At Ezekiel 40:24 the template is identified by the parameter-2 ketiv given here;
# the other site belongs to _KQ_POINTED_QERE_VERSES. Ezekiel 40:26's second note
# says the codex has a masorah circle but no qere note, which the policy treats as
# a denial; the verse's other מ:קו״כ-אם-2 stands in no note and remains.
# At Joshua 3:4 the note quotes מ"ק-א=ב', glossed as twice in this form with
# different spellings, one of the four named masorah-note policy choices.
_KQ_POINTED_KETIV_FAMILY = "מ:קו״כ-אם-2"
_KQ_POINTED_KETIV_VERSES = (
    (("B1-Joshua", "3", "4"), None),
    (("C3-Ezekiel", "40", "24"), "אילו"),
    (("C3-Ezekiel", "40", "25"), None),
    (("C3-Ezekiel", "40", "26"), None),
)
# At Ezekiel 40:24's second site the template is a מ:קו״כ-אם-2 too. The note records
# an explicit qere note in the Leningrad Codex, and attributes two masorah circles
# and the spelling with a yod before the final vav to the Aleppo Codex. It quotes
# מ"ק-א=<ד' מל>, four times written plene. Parameter 3, MAM's pointed qere, replaces
# the template and must equal that parenthesized form less its two HEBREW MARK
# MASORA CIRCLE, since masorah circles are excluded from the dataset.
# This named policy follows the spelling MAM's prose attributes to the codex;
# parameter 1 lacks that yod and is an alternative the policy does not take.
_KQ_POINTED_QERE_FAMILY = "מ:קו״כ-אם-2"
_KQ_POINTED_QERE_VERSES = ((("C3-Ezekiel", "40", "24"), "ואילמו"),)
# At these two MAM's ketiv, pointed by the transplant, replaces the template, by
# family. At Isaiah 26:20 the מ:כו״ק מיוחד's agreeing clause,
# '=א-כתיב אבל כדרכו אין הערת "קרי"', says the codex has MAM's ketiv and no qere
# note, without quoting a pointed form. The policy supplies the pointing by
# transplant; this is an inferred form, rather than a quoted manuscript form.
# At Zephaniah 2:9 the כו״ק's note says that the codex has only a simple masorah
# note, ל', and records an explicit qere note in the Leningrad Codex, without
# giving a codex form. The named policy points MAM's ketiv by transplant rather
# than leaving it unpointed or retaining the template.
_KQ_TRANSPLANT_VERSES = (
    (("C1-Isaiah", "26", "20"), "מ:כו״ק מיוחד"),
    (("CA-The-12-Minor-Prophets צפניה", "2", "9"), "כו״ק"),
)
# Of those two, the verse whose note must also have an agreeing clause whose first
# siglum is א-כתיב, saying that the codex has MAM's ketiv.
_KQ_TRANSPLANT_KETIV_AGREEING_VERSES = (("C1-Isaiah", "26", "20"),)
# The transplant takes the one longest matching of the qere's letters to the ketiv's,
# except at a verse this table names, a named exception. At Zephaniah 2:9 the
# qere, גּוֹיִ֖י, has two yods where the ketiv, גוי, has one, so there are two
# longest matchings. Matching the ketiv's yod to the qere's second yod leaves the
# first, with its hiriq and its accent, unmatched, so the tie is broken toward
# matching it to the first yod, which leaves no mark unplaced, and the ketiv pointed
# is גּוֹיִ֖.
_TRANSPLANT_TIE_BROKEN_VERSES = (("CA-The-12-Minor-Prophets צפניה", "2", "9"),)
# At Jeremiah 33:26 the template, a קו״כ, is kept: the note's א-כתיב form is
# doubt-marked, the note reasoning whether the codex's letter is a yod or a vav,
# so the evidence policy flags the doubtful reading rather than applying it. phase6_flags.py adds that flag to the note.
_KQ_KEPT_FAMILY = "קו״כ"
_KQ_KEPT_VERSES = (("C2-Jeremiah", "33", "26"),)
# The sigla heading a clause that quotes the codex's text of the atom.
_KQ_CODEX_HEADS = frozenset({"א", "א-כתיב"})
# A run in parentheses in a note's clause, where _prose_form looks for a form.
_PARENTHESIZED = re.compile(r"\(([^()]*)\)")

# The maqaf policy follows chapter 2 of MAM's introduction, section
# "עקביות במקפים". The table names 13 codex-citing differing clauses to apply:
# the verse, the exact clause head, separator difference and certainty.
#
# The clauses at Proverbs 3:30, 1 Chronicles 9:4 and 2 Kings 5:18 belong to the
# ketiv-plane work; 2 Samuel 8:3's א-קרי clause concerns the qere. Job 23:5 takes
# the first quoted form, which has MAM's merkha. Proverbs 3:30 is one of the
# survey's two prose cases, outside its 24 comparable clauses. Eleven of those
# 24 are outside the table: the three deferred clauses at 1 Chronicles 9:4,
# 2 Kings 5:18 and 2 Samuel 8:3, and eight doubt-marked clauses at seven verses
# (1 Samuel 31:2; 1 Kings 20:29; Isaiah 45:6 and twice at 59:19; Job 41:22;
# 1 Chronicles 18:4; 2 Chronicles 11:23).
_MAQAF_ADDED_AT_SPACE = "maqaf: clause form has a maqaf where the target had a space"
_MAQAF_ADDED_INSIDE_ATOM = "maqaf: clause form has a maqaf inside one target atom"
_MAQAF_REMOVED = "maqaf: clause form has a space where the target had a maqaf"
_MAQAF_ADDED = "maqaf: maqafs added"
_MAQAF_UNDOUBTED = "maqaf: undoubted clauses applied"
_MAQAF_BANG_MARKED = "maqaf: bang-marked clauses applied"
_MAQAF_READINGS = {
    ('BA-Samuel שמ"א', "14", "49"): (
        "א,ל,ק",
        _MAQAF_ADDED_INSIDE_ATOM,
        _MAQAF_UNDOUBTED,
    ),
    ("CA-The-12-Minor-Prophets מיכה", "5", "2"): (
        "א",
        _MAQAF_ADDED_AT_SPACE,
        _MAQAF_UNDOUBTED,
    ),
    ("D3-Job", "18", "15"): (
        'א,ל,מ"ש',
        _MAQAF_ADDED_INSIDE_ATOM,
        _MAQAF_UNDOUBTED,
    ),
    ("D3-Job", "21", "15"): ("א", _MAQAF_REMOVED, _MAQAF_UNDOUBTED),
    ("D3-Job", "23", "5"): (
        "א",
        _MAQAF_ADDED_AT_SPACE,
        _MAQAF_UNDOUBTED,
    ),
    ('FC-Chronicles דה"א', "9", "39"): (
        "א,ל",
        _MAQAF_ADDED_INSIDE_ATOM,
        _MAQAF_UNDOUBTED,
    ),
    ('FC-Chronicles דה"א', "10", "2"): (
        "א,ל,ש2?",
        _MAQAF_ADDED_INSIDE_ATOM,
        _MAQAF_UNDOUBTED,
    ),
    ('FC-Chronicles דה"א', "18", "17"): (
        "א",
        _MAQAF_ADDED_AT_SPACE,
        _MAQAF_UNDOUBTED,
    ),
    ("D1-Psalms", "75", "4"): (
        "א!",
        _MAQAF_ADDED_AT_SPACE,
        _MAQAF_BANG_MARKED,
    ),
    ('BA-Samuel שמ"ב', "12", "1"): (
        "א!",
        _MAQAF_REMOVED,
        _MAQAF_BANG_MARKED,
    ),
    ("CA-The-12-Minor-Prophets יואל", "2", "25"): (
        "א!",
        _MAQAF_REMOVED,
        _MAQAF_BANG_MARKED,
    ),
    ("D1-Psalms", "106", "48"): (
        "א!",
        _MAQAF_REMOVED,
        _MAQAF_BANG_MARKED,
    ),
    ("D1-Psalms", "107", "18"): (
        "א!,ש1",
        _MAQAF_REMOVED,
        _MAQAF_BANG_MARKED,
    ),
}
_MAQAF_DEFERRED_HEADS = frozenset({"א-כתיב", "א-קרי"})
_MAQAF_EXPECTED_CHANGE = {
    _MAQAF_ADDED_AT_SPACE: (" ", MAQAF),
    _MAQAF_ADDED_INSIDE_ATOM: ("", MAQAF),
    _MAQAF_REMOVED: (MAQAF, " "),
}
# In the transplant, a final letter matches its non-final form.
_NON_FINAL = str.maketrans("ךםןףץ", "כמנפצ")

# The hataf policy restores the vowel at each varika. Chapter 2 of MAM's
# introduction, section "חטפים באותיות לא גרוניות", says that MAM has a plain
# sheva with a varika where manuscripts have a hataf on a non-guttural letter
# (in/mam-ws-intro/ch2.mediawiki). A note saying the codex lacks the hataf would
# prevent restoration; no current note says so.
#
# The build reads each vowel from MAM's note and checks it against the independent
# three-rule inference in py/explicit_xataf/infer.py. At the five letters where
# chapter 2 attributes a hataf hiriq to the codex, the dataset has sheva plus hiriq,
# as MAM's notes write the form.
#
# The inference is: hataf qamats where the next letter is one of these gutturals
# with qamats or qamats qatan; hiriq, with sheva retained, where the next letter is
# a guttural with hiriq; hataf patah otherwise.
_GUTTURALS = frozenset("אהחע")
# A clause of a note body that quotes forms joins two of them with this word, "or".
_OR = "או"
# The template phase 2 replaces by HEBREW PUNCTUATION PASEQ in the body text, which
# stands in the bodies of the varika notes of 16 verses of Psalms. A note body is
# kept verbatim, so _clauses reads the template as the character phase 2 writes for
# it, which is what the target beside the body has.
_LEGARMEH = "מ:לגרמיה-2"
# At Jeremiah 31:32 the note's forms give two vowels. The clause headed ל quotes the
# target with a hataf patah, and a clause whose head names בן־אשר, most printed
# editions and Koren quotes it with a hataf qamats, citing no manuscript. The vowel
# is that of the clause headed ל, the one clause citing a manuscript for a hataf,
# and the inference gives the same vowel. The build raises unless the note still
# has exactly one clause headed ל giving a vowel, and a clause giving a different
# one.
_HATAF_FROM_LENINGRAD_VERSES = (("C2-Jeremiah", "31", "32"),)
_LENINGRAD_HEAD = "ל"
# At Psalms 17:14 no clause with sigla quotes the first note's target with the
# hataf. The note's agreeing clause says in prose that by the codex's practice there
# is a hataf as well, and quotes that form in angle brackets, so where no clause
# with sigla gives a vowel, the vowel is read from the forms in angle brackets in
# the note's agreeing clauses. The build raises unless that happens exactly once in
# the verse. It is the one site where MAM-basics' in/explicit-xataf-manual.json
# gives the form by hand.
_HATAF_FROM_AGREEING_VERSES = (("D1-Psalms", "17", "14"),)
_ANGLE_RUN = re.compile("<([^>]*)>")

# The stress-helper policy applies where the codex survives and where it is lost.
# MAM has pashta, segolta, telisha qetanah and zarqa on an atom's last letter,
# and telisha gedolah on its first. A stress helper is a second copy on the first
# letter of the stressed syllable; the zarqa's helper is Unicode ZARQA beside the
# zarqa's Unicode ZINOR.
#
# Sub-rule 1 removes pashta's stress helper only on the second-to-last letter,
# following the codex's rule as described in Yeivin section 239. A mater counts
# as an intervening letter. Sub-rule 2 removes the other four accents' helpers
# wherever they stand. Sub-rule 3 is phase 2's selection of parameter 1 of מ:דחי
# and מ:צינור. Sub-rule 4 is the telisha-gedolah table below, including the א(ס)
# testimony at Leviticus 10:4.
#
# Each entry below names an accent whose stress helper is removed, and the
# position where MAM has the accent itself: the last letter, or for telisha
# gedolah the first. The zarqa is found by its Unicode ZINOR.
_STRESS_HELPER_ACCENTS = {
    PASHTA: ("pashta", -1),
    SEGOLTA: ("segolta", -1),
    TELISHA_QETANA: ("telisha qetanah", -1),
    TELISHA_GEDOLA: ("telisha gedolah", 0),
    UNICODE_ZINOR: ("zarqa", -1),
}
# The poetic verses, where Unicode ZARQA is the tsinnorit and Unicode ZINOR the
# tsinnor, so that neither is a zarqa or its stress helper: all of Psalms and
# Proverbs, and Job 3:2 to 42:6, as MAM-basics bounds Job's poetic section.
_POETIC_BOOKS = ("D1-Psalms", "D2-Proverbs")
_JOB = "D3-Job"
_JOB_POETIC = ((3, 2), (42, 6))
# A note can override sub-rules 1 and 2: retain MAM's stress helper where an
# agreeing clause says the Aleppo Codex doubles the accent, or cites the Leningrad
# Codex for doubling and no clause cites the Aleppo Codex. These phrases identify
# that statement. The population snapshot pins the verses reached through ל.
# MAM-parsed-plus is the Scripture-and-note input; extantness is checked by the
# public census against aleppo/index-flat-annotated.json. The named ל sites are
# in lost portions of the Aleppo Codex.
_DOUBLING_PHRASES = ("טעם כפול", "הטעמה כפולה")
# The sigla of rule 4 for the codex's text and for testimony to its lost parts, as
# _clause_sigla reads them, each less any "!" or "?".
_STRESS_HELPER_CODEX_SIGLA = frozenset(
    {
        "א",
        "א-צילום",
        "א(צילום)",
        "א-כתיב",
        "א-קרי",
        "א-תיקון",
        "א[לאחר תיקון]",
        "א(ו)",
        "א(ס)",
        "א(ע)",
        "א(ק)",
        "א(ר)",
    }
)
# In a list of sigla, א(x,y) names the testimonies א(x) and א(y), and א(צילום ...)
# the photograph, as the census's nusach_aleppo_readings.py reads them.
_TESTIMONY_LIST = re.compile(r"^א\(([^)]*)\)$")
_PHOTOGRAPH = "צילום"
# Sub-rule 4, the five telisha-gedolah words: MAM has a geresh or a gershayim beside
# the telisha gedolah in five atoms, and only the atoms of Leviticus 10:4 and
# Ezekiel 48:10 have a stress helper. At each of those two the table names the mark
# that goes besides the stress helper, the letter it goes from, and the head of the
# note's clause whose first form the atom must then equal. At Ezekiel 48:10 the
# geresh on the stressed letter goes, as the sub-rule was first written, giving the
# form of the clause headed א. At Leviticus 10:4 MAM has the gershayim and the
# telisha gedolah on both the qof and the bet, and the note's ש1 ושיטת-א clause cites
# א(ס) for the telisha gedolah on the qof and the gershayim on the bet. Rule 4 counts
# א(ס) as Aleppo and admits שיטת-א only where the codex is lost, so the gershayim
# on the first letter goes, giving the form of the clause
# headed ל,ל1,ב,ש,ו?.
_HELPER_LETTER = "the stress helper's letter"
_FIRST_LETTER = "the atom's first letter"
_TELISHA_GEDOLA_WORDS = {
    ("A3-Levit", "10", "4"): (GERSHAYIM, _FIRST_LETTER, "ל,ל1,ב,ש,ו?"),
    ("C3-Ezekiel", "48", "10"): (GERESH, _HELPER_LETTER, "א"),
}
# The verses where the policy keeps a pashta's stress helper, a letter standing
# between, and a clause citing the codex quotes the atom with the pashta alone. A
# note's explicit codex form takes precedence over the positional rule, so these are phase 5's to apply, and four of the seven
# clauses are bang-marked, which phase 5 applies and flags.
_PASHTA_STRESS_HELPER_FOR_PHASE_5 = (
    ("A5-Deuter", "29", "28"),
    ('BA-Samuel שמ"ב', "11", "25"),
    ('BC-Kings מל"ב', "14", "7"),
    ("C1-Isaiah", "44", "8"),
    ('FC-Chronicles דה"א', "6", "45"),
    ('FC-Chronicles דה"א', "21", "12"),
    ('FC-Chronicles דה"ב', "6", "20"),
)
# A template in note bodies that _clauses reads as its parameter 2, the link's text.
# Ezekiel 16:12's note, whose target holds a pashta's stress helper, has one.
_LINK = "מ:קישור בהערה"
_INTERNAL_LINK = "מ:קישור פנימי בהערה"
_BOLD = "מודגש"

# Where a stretch of text sits. A policy changes its targets in both kinds of
# parameter and counts them apart; a target in a special-letter word raises.
_SELECTED = "selected"  # a selected parameter, or text outside templates
_UNSELECTED = "unselected"  # an unselected parameter of a kept ketiv/qere template
_FORBID = "forbid"  # a special-letter word phase 2 keeps

# The templates phase 2 leaves in the E column, by phase 2's action for them.
_KEPT_ACTIONS = (
    phase2._KEEP_NOTE,
    phase2._KEEP_KQ,
    phase2._VERBATIM,
    phase2._COLLAPSE_WORD,
)

_UNSELECTED_SUFFIX = " (unselected parameter)"

_QAMATS_QATAN = "HEBREW POINT QAMATS QATAN changed to HEBREW POINT QAMATS"
_ELOHIM_SHEVA = "Elohim reading: sheva for the hataf segol on the yod"
_ELOHIM_BARE_YOD = "Elohim reading: yod with no vowel, unchanged"
_ADONAI_HOLAM_STRIPPED = "Adonai reading: holam on the first he stripped"
_ADONAI_HOLAM_KEPT = "Adonai reading: holam kept where a note records the codex's"
_TITLE_HOLAM_STRIPPED = "divine title: holam on the dalet stripped"
_TITLE_HOLAM_KEPT = "divine title: holam kept where a note records the codex's"
_NOT_TITLE = "atom ending in אדני without a qamats on the nun, unchanged"
_REVIA_REMOVED = "revia mugrash: revia removed from the geresh muqdam's letter"
_REVIA_KEPT = "revia mugrash: revia kept where chapter 5 records the codex's"
_GERESH_MUQDAM_MOVED = "revia mugrash: geresh muqdam moved to the compound's first atom"
_REVIA_ELSEWHERE = "geresh muqdam with the revia on another letter, unchanged"
_REMOVAL_AS_QUOTED = "revia mugrash: removal agreeing with a codex form its note quotes"
_REMOVAL_QUOTED_WITHOUT_GERESH_MUQDAM = (
    "revia mugrash: removal whose note's codex form lacks the geresh muqdam too"
)
_OLE_REMOVED = "ole on the yored's letter: ole removed"
_OLE_REMOVED_OUTSIDE_NOTES = "ole on the yored's letter: removal in no note's target"
_OLE_WITHOUT_YORED = "ole on a letter without the yored, unchanged"
_OLE_REMOVAL_AS_QUOTED = (
    "ole on the yored's letter: removal agreeing with the codex form its note quotes"
)
_KQ_FORM_FROM_NOTE = (
    "ketiv/qere apparatus: template replaced by the codex form its note quotes"
)
_KQ_POINTED_KETIV = "ketiv/qere apparatus: template replaced by its pointed ketiv"
_KQ_POINTED_QERE = (
    "ketiv/qere apparatus: template replaced by its pointed qere, the spelling its "
    "note's prose gives the codex"
)
_KQ_TRANSPLANT = (
    "ketiv/qere apparatus: template replaced by MAM's ketiv pointed by the transplant"
)
_KQ_KEPT = "ketiv/qere apparatus: template kept where the codex form is doubt-marked"
_KQ_AGREES_WITH_FORM = (
    "ketiv/qere apparatus: transplant agreeing with the codex form a note quotes"
)
_KQ_AGREES_WITH_POINTED_KETIV = (
    "ketiv/qere apparatus: transplant agreeing with MAM's pointed ketiv"
)
_KQ_POINTED_QERE_AS_QUOTED = (
    "ketiv/qere apparatus: pointed qere equal to the form its note's prose gives the "
    "codex, less the form's masorah circles"
)
_HATAF_PATAH_RESTORED = (
    "hataf on a non-guttural: sheva and varika replaced by a hataf patah"
)
_HATAF_QAMATS_RESTORED = (
    "hataf on a non-guttural: sheva and varika replaced by a hataf qamats"
)
_HATAF_HIRIQ_RESTORED = (
    "hataf on a non-guttural: varika replaced by a hiriq, the sheva kept"
)
_HATAF_AS_QUOTED = (
    "hataf on a non-guttural: restoration agreeing with a form its note quotes"
)
_HATAF_FROM_LENINGRAD = (
    "hataf on a non-guttural: vowel from the clause headed ל, the forms disagreeing"
)
_HATAF_FROM_AGREEING = (
    "hataf on a non-guttural: vowel from the forms of the note's agreeing clause"
)

# The label of each vowel the hataf policy restores.
_HATAF_RESTORED = {
    HATAF_PATAH: _HATAF_PATAH_RESTORED,
    HATAF_QAMATS: _HATAF_QAMATS_RESTORED,
    HIRIQ: _HATAF_HIRIQ_RESTORED,
}
# The label of each verse table of the hataf policy.
_HATAF_TABLES = {
    _HATAF_FROM_LENINGRAD: _HATAF_FROM_LENINGRAD_VERSES,
    _HATAF_FROM_AGREEING: _HATAF_FROM_AGREEING_VERSES,
}

# What the stress-helper policy does with a stress helper, and why.
_STRIPPED = "stripped"
_BETWEEN = "kept, a letter standing between"
_KEPT_BY_CODEX = "kept by a note whose agreeing clause cites the codex for the doubling"
_KEPT_BY_LENINGRAD = (
    "kept by a note whose agreeing clause cites ל for the doubling, no clause "
    "citing the codex"
)
_STRESS_HELPER_KEPT_SITES = {
    _KEPT_BY_CODEX: "stress helpers: kept by a note citing the codex",
    _KEPT_BY_LENINGRAD: "stress helpers: kept by a note citing ל",
}
_STRIPPED_DESPITE_NOTE = (
    "stress helpers: stripped in the target of a note whose agreeing clause speaks "
    "of doubling"
)
_TELISHA_GEDOLA_WORD = (
    "stress helpers: geresh or gershayim removed with a telisha gedolah's stress "
    "helper"
)
_TELISHA_GEDOLA_WORD_AS_QUOTED = (
    "stress helpers: telisha-gedolah word equal to the form its table names"
)
_STRIPPED_AS_QUOTED = (
    "stress helpers: stripped stress helper's atom equal to a codex form its note "
    "quotes"
)
_KEPT_AS_QUOTED = (
    "stress helpers: kept stress helper's atom doubled in a codex form its note quotes"
)
_PASHTA_FOR_PHASE_5 = (
    "stress helpers: kept pashta's stress helper whose note quotes the codex's pashta "
    "alone"
)
# Each (accent, what the policy does) the policy counts: every accent's stress helper
# can be stripped or kept by a note, and only the pashta's kept for a letter between.
_STRESS_HELPER_TALLIES = [
    (accent, what)
    for accent in _STRESS_HELPER_ACCENTS
    for what in (_STRIPPED, _BETWEEN, _KEPT_BY_CODEX, _KEPT_BY_LENINGRAD)
    if what != _BETWEEN or accent == PASHTA
]


def _stress_helper_label(accent, what):
    """The label counting what the stress-helper policy did with ``accent``'s helpers."""
    return f"stress helpers: {_STRESS_HELPER_ACCENTS[accent][0]}'s stress helper {what}"


def _sites_by_verse(sites):
    """``sites``, each (verse, disposition, family, ketiv), as a dict from each verse to
    the (disposition, family, ketiv) of each of its sites, in the order given."""
    by_verse = {}
    for verse, *site in sites:
        by_verse[verse] = by_verse.get(verse, ()) + (tuple(site),)
    return by_verse


# Each verse the ketiv/qere apparatus's tables name, with each of its sites: the
# site's disposition, the family of its template, and, where a second note at the
# verse has a מ:קו״כ-אם-2, the consonantal ketiv, parameter 2, of the template the
# disposition is for. Ezekiel 40:24 has two sites, each naming its ketiv.
_KQ_SITES = _sites_by_verse(
    [
        (verse, _KQ_FORM_FROM_NOTE, family, None)
        for verse, family in _KQ_FORM_FROM_NOTE_VERSES
    ]
    + [
        (verse, _KQ_POINTED_KETIV, _KQ_POINTED_KETIV_FAMILY, ketiv)
        for verse, ketiv in _KQ_POINTED_KETIV_VERSES
    ]
    + [
        (verse, _KQ_POINTED_QERE, _KQ_POINTED_QERE_FAMILY, ketiv)
        for verse, ketiv in _KQ_POINTED_QERE_VERSES
    ]
    + [(verse, _KQ_TRANSPLANT, family, None) for verse, family in _KQ_TRANSPLANT_VERSES]
    + [(verse, _KQ_KEPT, _KQ_KEPT_FAMILY, None) for verse in _KQ_KEPT_VERSES]
)

# Expected counts and site lists live in in/near-aleppo/build-populations.json.
# The five public MAM instruments independently supply template, qamats,
# divine-name, Adonai and stress-helper populations. build_expectations.py maps
# only their mechanically supported counters into an input refresh.
#
# Policy effects have separate fixed checks: the three qamats-qatan removals
# caused by the ketiv/qere apparatus; the revia and ole exceptions; note evidence
# for apparatus replacements, restored hataf vowels and stress-helper decisions;
# selected-versus-unselected populations; and the maqaf table's outcomes.
# Every named note check re-derives its evidence from current MAM-parsed-plus.
# Reading dispositions, sensitive site lists and added-target counts are not
# inferred from these five census totals and remain fixed for review.

# The snapshot's site lists use main_build.py's verse names and build order.


class Policies:
    """Applies phase 3's policies verse by verse and tallies what they did."""

    def __init__(self):
        self.counts = Counter()
        self.sites = defaultdict(list)
        # Letters with both the geresh muqdam and the revia in the current verse.
        self._revia_mugrash_letters = 0
        # How many templates the apparatus replaced or kept in the current verse for
        # each of the verse's sites in _KQ_SITES.
        self._ketiv_qere_sites = Counter()
        # Notes in the current verse whose target the maqaf policy replaced.
        self._maqaf_notes = 0
        # The vowels a note decided for the varikas of its target that the walk has
        # not met yet, in order.
        self._hataf_waiting = []
        # The varikas in the current verse whose vowel each hataf table decided.
        self._hataf_table_uses = Counter()
        # What the innermost note being walked does with the stress helpers in its
        # target, as _stress_helper_note decides it: (what it keeps them for, or None,
        # and whether an agreeing clause speaks of doubling).
        self._stress_note = (None, False)
        # Telisha-gedolah words of sub-rule 4 in the current verse.
        self._telisha_gedola_words = 0
        # Forms quoting the codex's pashta alone at a kept stress helper, in the
        # current verse.
        self._pashta_for_phase_5 = 0

    def apply_e_cell(self, cell, verse):
        """Return one verse's E cell, as phase 2 resolved it, with the policies applied."""
        self._revia_mugrash_letters = 0
        self._ketiv_qere_sites = Counter()
        self._maqaf_notes = 0
        self._hataf_table_uses = Counter()
        self._telisha_gedola_words = 0
        self._pashta_for_phase_5 = 0
        cell = self._value(cell, verse, _SELECTED, None)
        if verse in _TELISHA_GEDOLA_WORDS and self._telisha_gedola_words != 1:
            raise AssertionError(
                f"{verse}: named in the telisha-gedolah word table, but "
                f"{self._telisha_gedola_words} such words are there, not 1"
            )
        if verse in _PASHTA_STRESS_HELPER_FOR_PHASE_5 and self._pashta_for_phase_5 != 1:
            raise AssertionError(
                f"{verse}: named in the phase 5 pashta table, but "
                f"{self._pashta_for_phase_5} forms citing the codex quote a kept "
                "pashta's atom with the pashta alone, not 1"
            )
        for label, verses in _HATAF_TABLES.items():
            if verse in verses and self._hataf_table_uses[label] != 1:
                raise AssertionError(
                    f"{verse}: named in a hataf table, but the table decided "
                    f"{self._hataf_table_uses[label]} varikas' vowels, not 1"
                )
        # A named verse with no such letter is one whose site lacks either mark.
        named = verse in _REVIA_KEPT_VERSES or verse in _GERESH_MUQDAM_MOVED_VERSES
        if named and self._revia_mugrash_letters != 1:
            raise AssertionError(
                f"{verse}: named in a revia-mugrash table, but "
                f"{self._revia_mugrash_letters} letters have both the geresh muqdam "
                "and the revia, not 1"
            )
        for site in _KQ_SITES.get(verse, ()):
            if self._ketiv_qere_sites[site] != 1:
                raise AssertionError(
                    f"{verse}: named in a ketiv/qere apparatus table for a {site[1]}, "
                    f"but {self._ketiv_qere_sites[site]} note targets hold that "
                    "template, not 1"
                )
        if verse in _MAQAF_READINGS and self._maqaf_notes != 1:
            raise AssertionError(
                f"{verse}: named in the maqaf table, but the policy applied at "
                f"{self._maqaf_notes} notes, not 1"
            )
        return cell

    def assert_expected_counts(self, expected_counts, expected_sites):
        """Require the populations in the provenance-bound expectation snapshot."""
        drift = [
            f"{label}: expected {expected}, build {self.counts[label]}"
            for label, expected in expected_counts.items()
            if self.counts[label] != expected
        ]
        drift += [
            f"{label}: expected at {expected}, build at {self.sites[label]}"
            for label, expected in expected_sites.items()
            if self.sites[label] != expected
        ]
        if drift:
            raise AssertionError("Phase 3 populations drifted: " + "; ".join(drift))

    def _value(self, value, verse, mode, note):
        """``note`` is the body of the innermost נוסח whose target holds ``value``."""
        if isinstance(value, str):
            return self._text(value, verse, mode, note)
        if isinstance(value, list):
            return [self._value(item, verse, mode, note) for item in value]
        return self._template(value, verse, mode, note)

    def _template(self, tmpl, verse, mode, note):
        name = tmpl["tmpl_name"]
        rule = phase2._RULES.get(name)
        if rule is None or rule.action not in _KEPT_ACTIONS:
            raise AssertionError(
                f"{verse}: phase 3 met {name!r}, a template phase 2 does not keep"
            )
        if rule.action == phase2._VERBATIM:
            return tmpl
        params = tmpl["tmpl_params"]
        if rule.action == phase2._COLLAPSE_WORD:
            self._text(params["2"], verse, _FORBID, note)
            return tmpl
        hataf = []
        stress_note = self._stress_note
        if name == _NOTE:
            note = params["2"]
            # The ketiv/qere apparatus runs first, then the maqaf policy; the
            # other policies walk the target those two leave.
            if mode == _SELECTED and verse in _KQ_SITES:
                params = dict(params)
                params["1"] = self._ketiv_qere_apparatus(params["1"], note, verse)
            if mode == _SELECTED:
                maqaf_target = self._maqaf_note(params["1"], note, verse)
                if maqaf_target != params["1"]:
                    params = dict(params)
                    params["1"] = maqaf_target
            self._stress_note = self._stress_helper_note(params["1"], note, verse)
            # The hataf's vowels are decided before the target is walked, and the
            # walk applies them.
            if mode == _SELECTED:
                hataf = self._hataf_decisions(params["1"], note, verse)
            if hataf and self._hataf_waiting:
                raise AssertionError(
                    f"{verse}: a note whose target holds a varika, inside the target "
                    "of another such note"
                )
            self._hataf_waiting += [vowel for _, vowel, _ in hataf]
        new_params = {}
        selected = phase2.selected_keys(tmpl, verse)
        for key, value in params.items():
            if key in selected:
                new_params[key] = self._value(value, verse, mode, note)
            elif rule.action == phase2._KEEP_KQ:
                unselected = _UNSELECTED if mode == _SELECTED else mode
                new_params[key] = self._value(value, verse, unselected, note)
            else:
                new_params[key] = value
        self._stress_note = stress_note
        if hataf and self._hataf_waiting:
            raise AssertionError(
                f"{verse}: the walk of a note's target met {len(self._hataf_waiting)} "
                "fewer varikas than the note's reading decided vowels for"
            )
        if name == _NOTE and mode == _SELECTED:
            self._check_revia_removals(params["1"], new_params["1"], note, verse)
            self._check_ole_removals(params["1"], new_params["1"], note, verse)
            self._check_hataf_restorations(params["1"], new_params["1"], hataf, verse)
            self._check_stress_helpers(params["1"], new_params["1"], note, verse)
        return {"tmpl_name": name, "tmpl_params": new_params}

    def _text(self, text, verse, mode, note):
        text = self._qamats_size(text, verse, mode)
        text = self._yhvh_elohim_vowel(text, verse, mode)
        text = self._divine_name_holam(text, verse, mode, note)
        text = self._adonai_holam(text, verse, mode, note)
        text = self._revia_mugrash(text, verse, mode)
        text = self._ole_on_yored(text, verse, mode, note)
        text = self._hataf(text, verse, mode)
        return self._stress_helpers(text, verse, mode)

    def _found(self, label, verse, mode, number=1):
        """Tally ``number`` targets of the policy ``label`` where ``mode`` says they are."""
        if mode == _FORBID:
            raise AssertionError(
                f"{verse}: {label}, inside a special-letter word phase 2 keeps"
            )
        self.counts[_tally_label(label, mode)] += number

    def _qamats_size(self, text, verse, mode):
        """Change every HEBREW POINT QAMATS QATAN to HEBREW POINT QAMATS.

        The codex does not distinguish the two qamats sizes, so in the dataset
        HEBREW POINT QAMATS is a qamats of either size, not a qamats gadol.
        """
        found = text.count(QAMATS_QATAN)
        if not found:
            return text
        self._found(_QAMATS_QATAN, verse, mode, found)
        return text.replace(QAMATS_QATAN, QAMATS)

    def _yhvh_elohim_vowel(self, text, verse, mode):
        """Put a sheva for the hataf segol on the yod of the Elohim reading.

        MAM's introduction gives a sheva on the yod as the manuscripts' custom, the
        pointing of the Adonai reading. An Elohim-reading atom whose yod has no
        vowel, which is Psalms 68:21's alone, has no hataf segol to replace.
        """
        edits = {}
        for atom in _atoms(text):
            found = _divine_name(text, atom, verse)
            if found is None or found[0] != _ELOHIM:
                continue
            yod_vowels = [i for i in found[1] if text[i] in _VOWELS]
            if [text[i] for i in yod_vowels] == [HATAF_SEGOL]:
                self._found(_ELOHIM_SHEVA, verse, mode)
                edits[yod_vowels[0]] = SHEVA
            elif not yod_vowels:
                self._found(_ELOHIM_BARE_YOD, verse, mode)
                self.sites[_ELOHIM_BARE_YOD].append(verse)
            else:
                raise AssertionError(
                    f"{verse}: an Elohim-reading divine name whose yod has a vowel "
                    "other than a lone hataf segol"
                )
        return _edited(text, edits)

    def _divine_name_holam(self, text, verse, mode, note):
        """Strip the holam on the first he of the Adonai reading, except where recorded.

        MAM's introduction says the manuscripts rarely have this holam and that
        MAM supplies it for the reader. Where a note on the atom opens with
        _CODEX_DIVINE_NAME_HOLAM_NOTE, MAM records the codex's holam, and the
        holam stays. 1 Kings 8:11's note has the same words without the siglum,
        so it says nothing about the codex, and the holam there is stripped. The Elohim reading keeps its holam, which the
        codex has.
        """
        edits = {}
        recorded = _note_opening(note).startswith(_CODEX_DIVINE_NAME_HOLAM_NOTE)
        for atom in _atoms(text):
            found = _divine_name(text, atom, verse)
            if found is None or found[0] != _ADONAI:
                continue
            holam = _lone_mark(
                text, found[2], HOLAM, verse, "the first he of a divine name"
            )
            if recorded:
                self._found(_ADONAI_HOLAM_KEPT, verse, mode)
                self.sites[_ADONAI_HOLAM_KEPT].append(verse)
            else:
                self._found(_ADONAI_HOLAM_STRIPPED, verse, mode)
                edits[holam] = ""
        return _edited(text, edits)

    def _adonai_holam(self, text, verse, mode, note):
        """Strip the holam on the dalet of the divine title, except where recorded.

        MAM's introduction says the codex has the title without a holam except in
        isolated places. The title is an atom whose letters end in אדני with a
        qamats on the nun; with any other vowel there the atom is the ordinary
        word, whose holam is a plain vowel and stays. Where a note on the atom
        opens with _CODEX_TITLE_HOLAM_NOTE, MAM records the codex's holam, and the
        holam stays: at Psalms 110:5 alone.
        """
        edits = {}
        recorded = _note_opening(note).startswith(_CODEX_TITLE_HOLAM_NOTE)
        for atom in _atoms(text):
            letters = "".join(text[index] for index, _ in atom[-4:])
            if len(atom) < 4 or letters != _ADONAI_LETTERS:
                continue
            (_, dalet_marks), (_, nun_marks) = atom[-3:-1]
            if QAMATS not in [text[i] for i in nun_marks]:
                if mode != _FORBID:
                    self.counts[_tally_label(_NOT_TITLE, mode)] += 1
                continue
            holam = _lone_mark(
                text, dalet_marks, HOLAM, verse, "the dalet of the title"
            )
            if recorded:
                self._found(_TITLE_HOLAM_KEPT, verse, mode)
                self.sites[_TITLE_HOLAM_KEPT].append(verse)
            else:
                self._found(_TITLE_HOLAM_STRIPPED, verse, mode)
                edits[holam] = ""
        return _edited(text, edits)

    def _revia_mugrash(self, text, verse, mode):
        """Remove the revia sharing a letter with the geresh muqdam, except where kept.

        MAM's introduction says MAM marks this revia consistently for the reader
        although the codex usually lacks it, and chapter 5 lists each letter with
        both marks and the codex's reading there. So such a letter loses its
        revia, except in the verses of _REVIA_KEPT_VERSES, where the revia stays,
        and of _GERESH_MUQDAM_MOVED_VERSES, where the geresh muqdam moves instead.
        A geresh muqdam whose atom has the revia on another letter stays as it
        is, and one whose atom has no revia raises.
        """
        edits = {}
        atoms = _atoms(text)
        for number, atom in enumerate(atoms):
            revias = [i for _, marks in atom for i in marks if text[i] == REVIA]
            for _, marks in atom:
                if GERESH_MUQDAM not in [text[i] for i in marks]:
                    continue
                geresh_muqdam = _lone_mark(
                    text, marks, GERESH_MUQDAM, verse, "a letter"
                )
                if REVIA not in [text[i] for i in marks]:
                    if not revias:
                        raise AssertionError(
                            f"{verse}: a geresh muqdam whose atom has no revia"
                        )
                    if mode != _FORBID:
                        self.counts[_tally_label(_REVIA_ELSEWHERE, mode)] += 1
                    continue
                revia = _lone_mark(
                    text, marks, REVIA, verse, "the geresh muqdam's letter"
                )
                self._revia_mugrash_letters += 1
                if verse in _REVIA_KEPT_VERSES:
                    self._found(_REVIA_KEPT, verse, mode)
                    self.sites[_REVIA_KEPT].append(verse)
                elif verse in _GERESH_MUQDAM_MOVED_VERSES:
                    self._found(_GERESH_MUQDAM_MOVED, verse, mode)
                    self.sites[_GERESH_MUQDAM_MOVED].append(verse)
                    sheva = _bemo_sheva(text, atoms, number, verse)
                    edits[geresh_muqdam] = ""
                    edits[sheva] = SHEVA + GERESH_MUQDAM
                else:
                    self._found(_REVIA_REMOVED, verse, mode)
                    edits[revia] = ""
        return _edited(text, edits)

    def _check_revia_removals(self, before, after, body, verse):
        """Check each revia removal in a note's target against the note's codex forms.

        A clause of the note citing one of _CODEX_SIGLA quotes the codex, and its
        form is MAM's statement of what the codex has, independent of the chapter
        5 list the policy follows. So where the policy removed a revia in the
        target, the letter must have the marks it has in each such form with the
        target's letters, a clause agreeing with MAM quoting the target as it
        was. _NOTE_FORM_WITHOUT_GERESH_MUQDAM_VERSES names any reviewed forms
        lacking the geresh muqdam too; it is empty since the 2026-09-17 input
        refresh. Any other difference raises, as does a removal whose note
        quotes no such form.
        """
        if verse in _REVIA_KEPT_VERSES or verse in _GERESH_MUQDAM_MOVED_VERSES:
            return
        target = _selected_text(before, verse)
        letters = _letters_and_marks(target)
        sites = [
            index
            for index, (_, marks) in enumerate(letters)
            if GERESH_MUQDAM in marks and REVIA in marks
        ]
        if not sites:
            return
        result = _letters_and_marks(_selected_text(after, verse))
        spelling = [letter for letter, _ in letters]
        forms = []
        for form in _codex_forms(body, verse):
            quoted = _letters_and_marks(target if form is None else form)
            if [letter for letter, _ in quoted] == spelling:
                forms.append(quoted)
        if not forms:
            raise AssertionError(
                f"{verse}: a revia removed in the target of a note quoting no codex "
                "form with the target's letters"
            )
        for index in sites:
            marks = result[index][1]
            for quoted in forms:
                if marks == quoted[index][1]:
                    self.counts[_REMOVAL_AS_QUOTED] += 1
                elif (
                    verse in _NOTE_FORM_WITHOUT_GERESH_MUQDAM_VERSES
                    and marks.replace(GERESH_MUQDAM, "") == quoted[index][1]
                ):
                    self.counts[_REMOVAL_QUOTED_WITHOUT_GERESH_MUQDAM] += 1
                    self.sites[_REMOVAL_QUOTED_WITHOUT_GERESH_MUQDAM].append(verse)
                else:
                    raise AssertionError(
                        f"{verse}: after the revia's removal its letter's marks "
                        "differ from a codex form the note quotes"
                    )

    def _ole_on_yored(self, text, verse, mode, note):
        """Remove the ole from a letter that also has the yored.

        MAM's introduction, chapter 2, says that where the yored's syllable begins
        its atom and the atom before is stressed on its last syllable or has a
        disjunctive, the manuscripts have the yored alone, while the printed
        editions have the ole on the yored's letter, as MAM has it for the reader.
        Chapter 5 lists the 13 verses where MAM has both marks on one letter, with
        the codex's form at each, and says that the codex lacks the ole in all of
        them. The criterion is mechanical, so no table names a verse. An ole on a
        letter without the yored stays as it is. A removal in no note's target is
        recorded apart, and _check_ole_removals checks the others against their
        notes.
        """
        edits = {}
        for atom in _atoms(text):
            for _, marks in atom:
                if OLE not in [text[i] for i in marks]:
                    continue
                ole = _lone_mark(text, marks, OLE, verse, "a letter")
                if YORED not in [text[i] for i in marks]:
                    if mode != _FORBID:
                        self.counts[_tally_label(_OLE_WITHOUT_YORED, mode)] += 1
                    continue
                _lone_mark(text, marks, YORED, verse, "the ole's letter")
                self._found(_OLE_REMOVED, verse, mode)
                self.sites[_OLE_REMOVED].append(verse)
                if note is None:
                    self.sites[_OLE_REMOVED_OUTSIDE_NOTES].append(verse)
                edits[ole] = ""
        return _edited(text, edits)

    def _check_ole_removals(self, before, after, body, verse):
        """Check each ole removal in a note's target against the note.

        A clause citing the codex is MAM's statement of what the codex has,
        independent of the criterion the policy follows. So where the policy
        removed an ole in the target, the note must have a clause whose head has a
        siglum that, less any "!" or "?", is _OLE_CODEX_SIGLUM, and every such
        clause must quote the target as the policies leave it: the text after the
        clause's "=", less a leading "<", starts with that target's text, followed
        by one of _OLE_AFTER_QUOTED_TARGET. The whole target is compared, not a form
        read up to its first space as _parsed_clauses reads one, because at Job 9:22
        the target and the form its clause quotes are two atoms. A clause opening
        with "=" whose sigla include that siglum raises as well, since it would give
        the codex MAM's form, the ole included.
        """
        target = _selected_text(before, verse)
        removals = sum(
            1
            for _, marks in _letters_and_marks(target)
            if OLE in marks and YORED in marks
        )
        if not removals:
            return
        for head, sigla, _ in _parsed_clauses(body, verse):
            if not head and _OLE_CODEX_SIGLUM in [s.rstrip("!?") for s in sigla]:
                raise AssertionError(
                    f"{verse}: an ole removed in the target of a note whose agreeing "
                    "clause cites the codex"
                )
        result = _selected_text(after, verse)
        citing = 0
        for clause in _clauses(body, verse):
            head, equals, rest = clause.partition("=")
            heads = [siglum.rstrip("!?") for siglum in head.split(",")]
            if not equals or _OLE_CODEX_SIGLUM not in heads:
                continue
            quoted = rest[1:] if rest.startswith("<") else rest
            follows = quoted[len(result) : len(result) + 1]
            if not quoted.startswith(result) or follows not in _OLE_AFTER_QUOTED_TARGET:
                raise AssertionError(
                    f"{verse}: a clause citing the codex does not quote the target "
                    "as the policies leave it"
                )
            citing += 1
        if not citing:
            raise AssertionError(
                f"{verse}: an ole removed in the target of a note with no clause "
                "citing the codex"
            )
        self.counts[_OLE_REMOVAL_AS_QUOTED] += removals

    def _ketiv_qere_apparatus(self, target, body, verse):
        """A note's target with its ketiv/qere template replaced, or kept, per _KQ_SITES.

        The template is the target's direct element of the family that one of the
        verse's sites in _KQ_SITES names, with the consonantal ketiv the site names
        where it names one. A target without one is returned as it is; one with more
        than one raises, as does a template whose parameters are not all plain text.
        The note must then say what the site's table assumes, or the build raises:

        - form from the note: exactly one clause headed א or א-כתיב, with no "!"
          or "?", whose form starts with the target's text before the template and
          ends with its text after it. What remains replaces the template. It must
          have the letters of the ketiv, or at Ezekiel 24:2 of the qere, and
          elsewhere it must equal the transplant of the qere onto the ketiv once
          HEBREW POINT QAMATS QATAN is changed to HEBREW POINT QAMATS in both;
        - pointed ketiv: no clause headed א or א-כתיב. Parameter 1 replaces the
          template, and must equal the transplant of parameter 3 onto parameter 2;
        - pointed qere: no clause headed א or א-כתיב, and one form in parentheses
          in the note's prose, as _prose_form reads it, with two HEBREW MARK MASORA
          CIRCLE. Parameter 3 replaces the template, and must equal that form less
          its circles;
        - transplant: no clause headed א or א-כתיב, and at a verse of
          _KQ_TRANSPLANT_KETIV_AGREEING_VERSES an agreeing clause whose first
          siglum is א-כתיב. The transplant of the qere onto the ketiv replaces the
          template;
        - kept: exactly one clause headed א or א-כתיב, headed א-כתיב, whose form
          ends in "?". The target stays as it is.

        A new target is stored as phase 2 stores a parameter.
        """
        elements = phase2._as_list(target)
        found = [
            (index, site)
            for site in _KQ_SITES[verse]
            for index, element in enumerate(elements)
            if isinstance(element, dict)
            and element["tmpl_name"] == site[1]
            and (site[2] is None or element["tmpl_params"].get("2") == site[2])
        ]
        if not found:
            return target
        if len(found) != 1:
            raise AssertionError(
                f"{verse}: a note's target has {len(found)} templates that the "
                "ketiv/qere apparatus's tables name, not 1"
            )
        ((index, site),) = found
        disposition, family, _ = site
        params = elements[index]["tmpl_params"]
        if not all(isinstance(value, str) for value in params.values()):
            raise AssertionError(
                f"{verse}: a {family} whose parameters are not all plain text"
            )
        clauses = _parsed_clauses(body, verse)
        headed = [
            (head, form)
            for head, _, form in clauses
            if any(siglum.rstrip("!?") in _KQ_CODEX_HEADS for siglum in head.split(","))
        ]
        if disposition == _KQ_FORM_FROM_NOTE:
            replacement = _note_form_less_target(elements, index, headed, verse)
            if verse not in _KQ_FORM_WITH_QERE_LETTERS_VERSES:
                pointed = _transplant(params["1"], params["2"], verse)
                if pointed.replace(QAMATS_QATAN, QAMATS) != replacement.replace(
                    QAMATS_QATAN, QAMATS
                ):
                    raise AssertionError(
                        f"{verse}: the transplant of the qere onto the ketiv differs "
                        "from the codex form the note quotes"
                    )
                self.counts[_KQ_AGREES_WITH_FORM] += 1
        elif disposition == _KQ_POINTED_KETIV:
            if headed:
                raise AssertionError(
                    f"{verse}: a note quoting the codex's form at a {family} whose "
                    "pointed ketiv is to replace it"
                )
            replacement = params["1"]
            if _transplant(params["2"], params["3"], verse) != replacement:
                raise AssertionError(
                    f"{verse}: the transplant of the pointed qere onto the ketiv "
                    "differs from the pointed ketiv"
                )
            self.counts[_KQ_AGREES_WITH_POINTED_KETIV] += 1
        elif disposition == _KQ_POINTED_QERE:
            if headed:
                raise AssertionError(
                    f"{verse}: a note quoting the codex's form at a {family} whose "
                    "pointed qere is to replace it"
                )
            replacement = params["3"]
            form = _prose_form(body, verse)
            if (
                form.count(MASORA_CIRCLE) != 2
                or form.replace(MASORA_CIRCLE, "") != replacement
            ):
                raise AssertionError(
                    f"{verse}: the form the note gives the codex in prose is not the "
                    "pointed qere with two HEBREW MARK MASORA CIRCLE"
                )
            self.counts[_KQ_POINTED_QERE_AS_QUOTED] += 1
        elif disposition == _KQ_TRANSPLANT:
            agreeing = [sigla[0] for head, sigla, _ in clauses if not head]
            if headed or (
                verse in _KQ_TRANSPLANT_KETIV_AGREEING_VERSES
                and "א-כתיב" not in agreeing
            ):
                raise AssertionError(
                    f"{verse}: the note at a {family} to point by the transplant "
                    "quotes the codex's form, or lacks the agreeing clause under the "
                    "siglum א-כתיב that its table assumes"
                )
            replacement = _transplant(params["1"], params["2"], verse)
        else:
            if (
                len(headed) != 1
                or headed[0][0] != "א-כתיב"
                or not headed[0][1].endswith("?")
            ):
                raise AssertionError(
                    f"{verse}: the note at a kept {family} lacks one doubt-marked "
                    "clause headed א-כתיב"
                )
            replacement = None
        self._ketiv_qere_sites[site] += 1
        self.counts[disposition] += 1
        self.sites[disposition].append(verse)
        if replacement is None:
            return target
        elements = elements[:index] + [replacement] + elements[index + 1 :]
        return phase2._simplify(phase2._merge_strings(elements))

    def _maqaf_note(self, target, body, verse):
        """Return a note's target with the tabled maqaf form, where applicable.

        Every differing clause citing the codex under phase 5's qualification 1
        is also the population check. A doubt-marked clause and a clause headed
        א-כתיב or א-קרי are outside this policy. Where one of the remaining
        clause's quoted forms has the target's letters and marks and differs only
        in spaces and maqafs, its verse and exact head must be in
        _MAQAF_READINGS. The first such form of the tabled clause is the target
        this policy returns.
        """
        text = _selected_text(target, verse)
        expected = _MAQAF_READINGS.get(verse)
        tabled_clauses = []
        candidates = []
        for clause in _clauses(body, verse):
            head, equals, rest = clause.partition("=")
            if not equals or not head:
                continue
            if expected is not None and head == expected[0]:
                tabled_clauses.append(rest)
            sigla = _qualified_codex_sigla(head)
            if not sigla or any("?" in qualifier for _, qualifier in sigla):
                continue
            if _MAQAF_DEFERRED_HEADS.intersection(siglum for siglum, _ in sigla):
                continue
            for form in _quoted_forms(rest):
                if form.endswith("?"):
                    continue
                changes = _maqaf_changes(text, form)
                if changes:
                    candidates.append((head, form, changes, sigla))
                    break

        unexpected = [
            head
            for head, _, _, _ in candidates
            if expected is None or head != expected[0]
        ]
        if unexpected:
            raise AssertionError(
                f"{verse}: maqaf-differing codex clause heads not in the policy "
                f"table: {unexpected}"
            )
        if expected is None:
            return target

        head, kind, certainty = expected
        if not tabled_clauses:
            return target
        if len(tabled_clauses) != 1:
            raise AssertionError(
                f"{verse}: the maqaf table's head {head!r} occurs in "
                f"{len(tabled_clauses)} clauses, not 1"
            )
        matching = [candidate for candidate in candidates if candidate[0] == head]
        if not matching:
            return target
        if len(matching) != 1:
            raise AssertionError(
                f"{verse}: the maqaf table's head {head!r} has {len(matching)} "
                "matching clauses, not 1"
            )
        _, form, changes, sigla = matching[0]
        if len(changes) != 1:
            raise AssertionError(
                f"{verse}: the maqaf table's form has {len(changes)} separator "
                "differences, not 1"
            )
        old, new = changes[0]
        if (old, new) != _MAQAF_EXPECTED_CHANGE[kind]:
            raise AssertionError(
                f"{verse}: the maqaf table calls the change {kind!r}, but it is "
                f"{old!r} to {new!r}"
            )
        qualifiers = [qualifier for _, qualifier in sigla]
        actual_certainty = _MAQAF_BANG_MARKED if "!" in qualifiers else _MAQAF_UNDOUBTED
        if actual_certainty != certainty:
            raise AssertionError(
                f"{verse}: the maqaf table calls the clause {certainty!r}, but its "
                f"codex sigla make it {actual_certainty!r}"
            )

        labels = [certainty]
        if new == MAQAF:
            labels.append(_MAQAF_ADDED)
            if kind == _MAQAF_ADDED_INSIDE_ATOM:
                labels.append(_MAQAF_ADDED_INSIDE_ATOM)
        else:
            labels.append(_MAQAF_REMOVED)
        for label in labels:
            self._found(label, verse, _SELECTED)
            self.sites[label].append(verse)
        self._maqaf_notes += 1
        # This module's docstring says the ketiv/qere apparatus is alone among these
        # policies in replacing a template. Returning ``form`` puts a flat string where
        # the target was, so a target holding a template would both falsify that claim
        # and lose the template. Every replaced target is a plain string today; the
        # assertion makes that a guarantee rather than a property of this data.
        if _holds_template(target):
            raise AssertionError(
                f"{verse}: the maqaf policy would replace a target holding a template "
                "with flat text, which only the ketiv/qere apparatus does"
            )
        return form

    def _hataf_decisions(self, target, body, verse):
        """The vowel of each varika in a note's target, in order, read from the note.

        A letter of the target is the letter _letters_and_marks finds in the
        target's selected text. For each letter with a varika, each form a clause
        with sigla quotes (_quoted_forms) is aligned with the target, and the
        form's aligned letter gives a vowel or nothing (_hataf_vowel). The aligned
        letter is the letter at the varika's position in the form's first atom
        whose letters are those of the varika's atom, or else the letter
        _only_match finds. Every form that gives a vowel must give the same one,
        and at least one must, except at the verses of _HATAF_FROM_LENINGRAD_VERSES
        and _HATAF_FROM_AGREEING_VERSES, whose comments say how the vowel is read
        there. The inference must then give the same vowel, or the build raises.

        Return (letter index, vowel, marks) for each varika, where marks lists the
        marks of the aligned letter in each form that gave the vowel.
        """
        text = _selected_text(target, verse)
        if VARIKA not in text:
            return []
        letters = _letters_and_marks(text)
        spelling = "".join(letter for letter, _ in letters).translate(_NON_FINAL)
        # For each letter, its atom's letters and its position in the atom.
        places = [
            ("".join(text[index] for index, _ in atom), position)
            for atom in _atoms(text)
            for position in range(len(atom))
        ]
        quoting, agreeing = _hataf_forms(body, verse)
        decisions = []
        for index, (_, marks) in enumerate(letters):
            if VARIKA not in marks:
                continue
            if marks.count(VARIKA) != 1:
                raise AssertionError(f"{verse}: a letter with more than one varika")
            site = (places[index], spelling, index)
            by_clause = [(head, _vowels_given(forms, *site)) for head, forms in quoting]
            vowels = [pair for _, pairs in by_clause for pair in pairs]
            if not vowels and verse in _HATAF_FROM_AGREEING_VERSES:
                vowels = _vowels_given(agreeing, *site)
                self._hataf_table_uses[_HATAF_FROM_AGREEING] += 1
                self.sites[_HATAF_FROM_AGREEING].append(verse)
            if (
                len({vowel for vowel, _ in vowels}) > 1
                and verse in _HATAF_FROM_LENINGRAD_VERSES
            ):
                leningrad = [
                    pairs
                    for head, pairs in by_clause
                    if head == _LENINGRAD_HEAD and pairs
                ]
                if len(leningrad) != 1:
                    raise AssertionError(
                        f"{verse}: the note has {len(leningrad)} clauses headed "
                        f"{_LENINGRAD_HEAD} giving a vowel, not 1"
                    )
                vowels = leningrad[0]
                self._hataf_table_uses[_HATAF_FROM_LENINGRAD] += 1
                self.sites[_HATAF_FROM_LENINGRAD].append(verse)
            distinct = {vowel for vowel, _ in vowels}
            if len(distinct) != 1:
                raise AssertionError(
                    f"{verse}: the forms of a varika's note give {len(distinct)} "
                    "vowels, not 1"
                )
            (vowel,) = distinct
            if _inferred_hataf(letters, index) != vowel:
                raise AssertionError(
                    f"{verse}: the vowel a varika's note gives, "
                    f"{unicodedata.name(vowel)}, is not the vowel the inference gives"
                )
            decisions.append((index, vowel, [aligned for _, aligned in vowels]))
        return decisions

    def _hataf(self, text, verse, mode):
        """Restore the hataf at each varika, with the vowel its note's reading decided.

        MAM has a sheva and a varika on a letter where the manuscripts have a
        hataf on a non-guttural. Each varika takes the next vowel _hataf_decisions
        left waiting. A hataf patah or a hataf qamats replaces the sheva, and the
        varika goes. For a hiriq, the varika is replaced by the hiriq and the sheva
        stays, which is how MAM's notes write the codex's hataf hiriq. The other
        marks on the letter stay in MAM's order.

        A varika raises in four places: where no vowel is waiting, which is a
        varika in no note's target; on no letter; not immediately after its
        letter's one sheva; and in an unselected parameter, since a note decides
        the vowels of its target's selected text alone. Through _found, a varika in
        a special-letter word raises too.
        """
        if VARIKA not in text:
            return text
        edits = {}
        met = 0
        for atom in _atoms(text):
            for _, marks in atom:
                if VARIKA not in [text[i] for i in marks]:
                    continue
                varika = _lone_mark(text, marks, VARIKA, verse, "a letter")
                met += 1
                if mode == _UNSELECTED:
                    raise AssertionError(
                        f"{verse}: a varika in an unselected parameter, where no "
                        "note decides its vowel"
                    )
                if not self._hataf_waiting:
                    raise AssertionError(
                        f"{verse}: a varika with no vowel waiting, in no note's target"
                    )
                vowel = self._hataf_waiting.pop(0)
                label = _HATAF_RESTORED[vowel]
                self._found(label, verse, mode)
                sheva = _lone_mark(text, marks, SHEVA, verse, "a varika's letter")
                if sheva != varika - 1:
                    raise AssertionError(
                        f"{verse}: a varika not immediately after its letter's sheva"
                    )
                if vowel == HIRIQ:
                    self.sites[label].append(verse)
                    edits[varika] = HIRIQ
                else:
                    edits[sheva] = vowel
                    edits[varika] = ""
        if met != text.count(VARIKA):
            raise AssertionError(f"{verse}: a varika on no letter")
        return _edited(text, edits)

    def _check_hataf_restorations(self, before, after, decisions, verse):
        """Check each hataf restored in a note's target against the note's forms.

        ``decisions`` is what _hataf_decisions returned for the note. At each
        restored letter, the letter's marks as the policies leave them must equal,
        mark for mark and in order, the marks of the aligned letter in at least one
        of the forms that gave the vowel, or the build raises.
        """
        if not decisions:
            return
        target = _letters_and_marks(_selected_text(before, verse))
        result = _letters_and_marks(_selected_text(after, verse))
        if [letter for letter, _ in result] != [letter for letter, _ in target]:
            raise AssertionError(f"{verse}: the policies changed a target's letters")
        for index, _, quoted in decisions:
            if result[index][1] not in quoted:
                raise AssertionError(
                    f"{verse}: a restored hataf's letter has marks that no form its "
                    "note quotes has"
                )
            self.counts[_HATAF_AS_QUOTED] += 1

    def _stress_helper_note(self, target, body, verse):
        """What a note does with the stress helpers in its target: (keeps, speaks).

        speaks is whether an agreeing clause of the note, one opening with "=", says
        that a manuscript doubles the accent, in one of _DOUBLING_PHRASES. keeps is
        what the qualification keeps the stress helpers for: _KEPT_BY_CODEX where
        such a clause's sigla include one of _STRESS_HELPER_CODEX_SIGLA,
        _KEPT_BY_LENINGRAD where they include ל and no clause of the note has sigla
        including one of _STRESS_HELPER_CODEX_SIGLA, and None otherwise. Sigla are
        read by _clause_sigla.

        Where such a clause's sigla include one citing the codex, or ל, the target
        must have exactly one atom with a stress helper, or the build raises. The
        body is read only where the target has a stress helper or the body's text
        has one of the phrases.
        """
        text = _selected_text(target, verse)
        with_helper = sum(
            1 for atom in _atoms(text) if _stress_helpers_of(text, atom, verse)
        )
        if not with_helper and not _has_doubling_phrase(body):
            return None, False
        clauses = [(clause, _clause_sigla(clause)) for clause in _clauses(body, verse)]
        cites_codex = any(
            _STRESS_HELPER_CODEX_SIGLA.intersection(sigla) for _, sigla in clauses
        )
        keeps, speaks = None, False
        for clause, sigla in clauses:
            if not clause.startswith("=") or not any(
                phrase in clause for phrase in _DOUBLING_PHRASES
            ):
                continue
            speaks = True
            codex = bool(_STRESS_HELPER_CODEX_SIGLA.intersection(sigla))
            leningrad = _LENINGRAD_HEAD in sigla
            if (codex or leningrad) and with_helper != 1:
                raise AssertionError(
                    f"{verse}: a note citing a manuscript for a doubled accent, whose "
                    f"target has {with_helper} atoms with a stress helper, not 1"
                )
            if codex:
                keeps = _KEPT_BY_CODEX
            elif leningrad and not cites_codex and keeps is None:
                keeps = _KEPT_BY_LENINGRAD
        return keeps, speaks

    def _stress_helpers(self, text, verse, mode):
        """Strip the stress helpers, by sub-rules 1, 2 and 4, except where kept.

        Sub-rule 1 strips the pashta's stress helper where it is on the atom's
        second-to-last letter and keeps it where a letter, a mater included,
        stands between it and the last letter. Sub-rule 2 strips the stress
        helpers of the segolta, the telisha qetanah, the telisha gedolah and the
        zarqa, wherever they stand. The qualification overrides both: where the
        innermost note whose target holds the atom keeps its stress helpers
        (_stress_helper_note), the stress helper stays. Where a telisha gedolah's
        stress helper goes, sub-rule 4 may take a geresh or a gershayim with it
        (_telisha_gedola_word). The other marks stay in MAM's order.

        _stress_helpers_of says what counts as a stress helper, and raises on an
        atom whose copies of an accent are in any other arrangement.
        """
        edits = {}
        keeps, speaks = self._stress_note
        for atom in _atoms(text):
            for accent, helper, position in _stress_helpers_of(text, atom, verse):
                if accent == PASHTA and position != len(atom) - 2:
                    what = _BETWEEN
                elif keeps is not None:
                    what = keeps
                    self.sites[_STRESS_HELPER_KEPT_SITES[keeps]].append(verse)
                else:
                    what = _STRIPPED
                    edits[helper] = ""
                    if speaks:
                        self.sites[_STRIPPED_DESPITE_NOTE].append(verse)
                self._found(_stress_helper_label(accent, what), verse, mode)
                if accent == TELISHA_GEDOLA:
                    edits.update(
                        self._telisha_gedola_word(
                            text, atom, position, what, verse, mode
                        )
                    )
        return _edited(text, edits)

    def _telisha_gedola_word(self, text, atom, position, what, verse, mode):
        """The edit sub-rule 4 makes to an atom whose telisha gedolah has a stress
        helper on letter ``position``, the stress helper having been ``what``.

        An atom with neither a geresh nor a gershayim needs no edit. One with either
        must be at a verse of _TELISHA_GEDOLA_WORDS, and its stress helper must
        have been stripped, or the build raises. The mark the table names then goes
        from the letter it names, which must have exactly one such mark.
        """
        marks = [text[i] for _, letter_marks in atom for i in letter_marks]
        if GERESH not in marks and GERSHAYIM not in marks:
            return {}
        if verse not in _TELISHA_GEDOLA_WORDS or what != _STRIPPED:
            raise AssertionError(
                f"{verse}: a telisha gedolah whose stress helper is {what}, in an atom "
                "with a geresh or a gershayim, is not a word the sub-rule 4 table names"
            )
        mark, letter, _ = _TELISHA_GEDOLA_WORDS[verse]
        marks_of = atom[position][1] if letter == _HELPER_LETTER else atom[0][1]
        index = _lone_mark(text, marks_of, mark, verse, letter)
        self._found(_TELISHA_GEDOLA_WORD, verse, mode)
        self.sites[_TELISHA_GEDOLA_WORD].append(verse)
        self._telisha_gedola_words += 1
        return {index: ""}

    def _check_stress_helpers(self, before, after, body, verse):
        """Check each stress helper in a note's target against the note's codex forms.

        A clause with sigla before its "=", one of which, as _clause_sigla reads
        them, is in _STRESS_HELPER_CODEX_SIGLA, quotes the codex, and each form it
        quotes (_quoted_forms) is MAM's statement of what the codex has, independent
        of the sub-rules the policy follows. For each atom of the target with a
        stress helper, _matching_atom finds the atom of each such form with the same
        letters; a form without one, or whose atom lacks the accent, is passed over.

        - Where the policy stripped the stress helper, the form's atom must equal,
          character for character, the target's atom as the policies leave it.
        - Where the policy kept it, the form's atom must have the accent on two
          letters, except at the verses of _PASHTA_STRESS_HELPER_FOR_PHASE_5, where
          a form may have the pashta on one letter.

        Any other form raises. At a verse of _TELISHA_GEDOLA_WORDS, the atom the
        policies leave must also equal the first form of the one clause whose head
        is the table's.
        """
        target = _selected_text(before, verse)
        sites = [
            (number, accent)
            for number, atom in enumerate(_atoms(target))
            for accent, _, _ in _stress_helpers_of(target, atom, verse)
        ]
        if not sites:
            return
        result = _selected_text(after, verse)
        if _spelling(result) != _spelling(target):
            raise AssertionError(f"{verse}: the policies changed a target's letters")
        atoms = _atoms(result)
        quoting, _ = _hataf_forms(body, verse)
        forms = [
            form
            for head, head_forms in quoting
            if _STRESS_HELPER_CODEX_SIGLA.intersection(_head_sigla(head))
            for form in head_forms
        ]
        for number, accent in sites:
            atom = atoms[number]
            left = _atom_text(result, atom)
            letters = "".join(result[index] for index, _ in atom)
            kept = accent in [a for a, _, _ in _stress_helpers_of(result, atom, verse)]
            if accent == TELISHA_GEDOLA and verse in _TELISHA_GEDOLA_WORDS:
                _, _, named = _TELISHA_GEDOLA_WORDS[verse]
                named_forms = [found for head, found in quoting if head == named]
                if len(named_forms) != 1 or named_forms[0][:1] != [left]:
                    raise AssertionError(
                        f"{verse}: a telisha-gedolah word the policies leave is not the "
                        f"first form of the one clause headed {named}"
                    )
                self.counts[_TELISHA_GEDOLA_WORD_AS_QUOTED] += 1
            for form in forms:
                quoted = _matching_atom(form, letters)
                if quoted is None or accent not in [
                    form[i] for _, m in quoted for i in m
                ]:
                    continue
                doubled = [a for a, _, _ in _stress_helpers_of(form, quoted, verse)]
                if not kept:
                    if _atom_text(form, quoted) != left:
                        raise AssertionError(
                            f"{verse}: a codex form the note quotes differs from an "
                            "atom whose stress helper the policy stripped"
                        )
                    self.counts[_STRIPPED_AS_QUOTED] += 1
                elif accent in doubled:
                    self.counts[_KEPT_AS_QUOTED] += 1
                elif accent == PASHTA and verse in _PASHTA_STRESS_HELPER_FOR_PHASE_5:
                    self._pashta_for_phase_5 += 1
                    self.sites[_PASHTA_FOR_PHASE_5].append(verse)
                else:
                    raise AssertionError(
                        f"{verse}: a codex form the note quotes lacks the stress helper "
                        "the policy kept"
                    )


def _tally_label(label, mode):
    """``label`` as it is counted in a selected or an unselected parameter."""
    return label if mode == _SELECTED else label + _UNSELECTED_SUFFIX


def _atoms(text):
    """The atoms of ``text``, each a list of (letter index, [indices of its marks])."""
    atoms, clusters = [], []
    for index, char in enumerate(text):
        if char.isspace() or char == MAQAF:
            if clusters:
                atoms.append(clusters)
            clusters = []
        elif char in _LETTERS:
            clusters.append((index, []))
        elif char in _MARKS and clusters:
            clusters[-1][1].append(index)
    if clusters:
        atoms.append(clusters)
    return atoms


def _letters_and_marks(text):
    """Each letter of ``text``, atom after atom, with its marks as a string."""
    return [
        (text[index], "".join(text[i] for i in marks))
        for atom in _atoms(text)
        for index, marks in atom
    ]


def _spelling(text):
    """The letters of ``text``, as _letters_and_marks finds them, without their marks."""
    return "".join(letter for letter, _ in _letters_and_marks(text))


def _transplant(ketiv, qere, verse):
    """``ketiv`` pointed by the letter-driven transplant of ``qere``'s marks.

    The transplant is letter-driven: each mark of the qere goes onto the ketiv's copy of the letter it
    sits on in the qere, a letter of the ketiv matched to no letter of the qere,
    such as an extra vav, gets no marks, and the qere's trailing maqaf is kept.
    The qere's letters are matched to the ketiv's in order, by longest common
    subsequence, a final letter matching its non-final form, and each letter of
    the ketiv, as the ketiv spells it, takes the marks of its matched letter, in
    MAM's order. Raise unless the ketiv is letters alone, the qere is letters with
    their marks and at most a trailing maqaf, exactly one longest matching exists,
    and every unmatched letter of the qere lacks marks. The one named exception to
    the rule of one longest matching is a verse of _TRANSPLANT_TIE_BROKEN_VERSES,
    where _tie_broken keeps, of several, the one that leaves no mark unplaced.

    Phase 4, which is deferred, would transplant at every consonantal ketiv with a
    qere; the ketiv/qere apparatus uses the transplant at the verses of _KQ_SITES.
    """
    if not ketiv or any(char not in _LETTERS for char in ketiv):
        raise AssertionError(f"{verse}: a ketiv to point that is not letters alone")
    maqaf = MAQAF if qere.endswith(MAQAF) else ""
    letters = _letters_and_marks(qere)
    if "".join(letter + marks for letter, marks in letters) + maqaf != qere:
        raise AssertionError(
            f"{verse}: a qere holding more than letters, their marks and a trailing "
            "maqaf"
        )
    matchings = _longest_matchings(
        ketiv.translate(_NON_FINAL), _spelling(qere).translate(_NON_FINAL)
    )
    if verse in _TRANSPLANT_TIE_BROKEN_VERSES:
        matchings = _tie_broken(matchings, letters, verse)
    if len(matchings) != 1:
        raise AssertionError(
            f"{verse}: {len(matchings)} longest matchings of the qere's letters to "
            "the ketiv's, not 1"
        )
    matched = dict(matchings[0])
    unmatched = set(range(len(letters))) - set(matched.values())
    if any(letters[index][1] for index in unmatched):
        raise AssertionError(
            f"{verse}: a letter of the qere that has marks matches no letter of the "
            "ketiv"
        )
    pointed = "".join(
        char + (letters[matched[index]][1] if index in matched else "")
        for index, char in enumerate(ketiv)
    )
    return pointed + maqaf


def _tie_broken(matchings, letters, verse):
    """Of several longest ``matchings``, the one that leaves no letter of the qere
    that has marks unmatched, ``letters`` being the qere's letters with their marks,
    as _letters_and_marks gives them.

    _TRANSPLANT_TIE_BROKEN_VERSES names ``verse``, so there must be a tie to break,
    two or more longest matchings, and exactly one of them must place every mark.
    """
    if len(matchings) < 2:
        raise AssertionError(
            f"{verse}: named in _TRANSPLANT_TIE_BROKEN_VERSES, but with "
            f"{len(matchings)} longest matchings of the qere's letters to the ketiv's, "
            "no tie to break"
        )
    placing = [
        matching
        for matching in matchings
        if not any(
            marks
            for index, (_, marks) in enumerate(letters)
            if index not in {qere_index for _, qere_index in matching}
        )
    ]
    if len(placing) != 1:
        raise AssertionError(
            f"{verse}: {len(placing)} of the longest matchings leave no letter of the "
            "qere that has marks unmatched, not 1"
        )
    return placing


def _longest_matchings(ketiv, qere):
    """Every longest in-order matching of the letters of ``ketiv`` to those of ``qere``.

    Each matching is a tuple of (ketiv index, qere index) pairs. A matching is
    built from its first pair, so no matching is listed twice.
    """
    lengths = {}

    def longest(i, j):
        if (i, j) not in lengths:
            lengths[i, j] = max(
                (
                    1 + longest(p + 1, q + 1)
                    for p in range(i, len(ketiv))
                    for q in range(j, len(qere))
                    if ketiv[p] == qere[q]
                ),
                default=0,
            )
        return lengths[i, j]

    def matchings(i, j):
        if longest(i, j) == 0:
            return [()]
        return [
            ((p, q),) + rest
            for p in range(i, len(ketiv))
            for q in range(j, len(qere))
            if ketiv[p] == qere[q] and 1 + longest(p + 1, q + 1) == longest(i, j)
            for rest in matchings(p + 1, q + 1)
        ]

    return matchings(0, 0)


def _divine_name(text, atom, verse):
    """For an atom whose letters end in יהוה: its reading, and the mark indices of
    its yod and of its first he.

    The vowel on the vav tells the readings apart, a hiriq for the Elohim reading
    and a qamats for the Adonai reading. A vav with neither, or both, raises.
    Return None for any other atom.
    """
    letters = "".join(text[index] for index, _ in atom[-4:])
    if len(atom) < 4 or letters != _DIVINE_NAME_LETTERS:
        return None
    (_, yod_marks), (_, he_marks), (_, vav_marks), _ = atom[-4:]
    vav = [text[i] for i in vav_marks]
    if (HIRIQ in vav) == (QAMATS in vav):
        raise AssertionError(
            f"{verse}: a divine name whose vav has neither a hiriq nor a qamats, or both"
        )
    return (_ELOHIM if HIRIQ in vav else _ADONAI), yod_marks, he_marks


def _bemo_sheva(text, atoms, number, verse):
    """The index of the sheva on the bet of _BEMO, the atom before atom ``number``.

    Raise unless the atom before atom ``number`` is _BEMO, letter for letter and
    mark for mark, and a maqaf alone stands between the two atoms.
    """
    before = atoms[number - 1] if number else []
    spelled = [(text[index], [text[i] for i in marks]) for index, marks in before]
    if spelled == _BEMO:
        last_index, last_marks = before[-1]
        end = max([last_index] + last_marks) + 1
        if text[end : atoms[number][0][0]] == MAQAF:
            return before[0][1][1]
    raise AssertionError(
        f"{verse}: the geresh muqdam to move is not in the atom after במו and a maqaf"
    )


def _separator_parts(text):
    """Return non-separator characters and the spaces or maqafs between them."""
    characters, separators, current = [], [], ""
    for char in text:
        if char in (" ", MAQAF):
            current += char
        else:
            separators.append(current)
            current = ""
            characters.append(char)
    separators.append(current)
    return characters, separators


def _maqaf_changes(target, form):
    """Separator pairs where ``target`` and ``form`` differ; None if text differs."""
    target_chars, target_separators = _separator_parts(target)
    form_chars, form_separators = _separator_parts(form)
    if target_chars != form_chars:
        return None
    return [
        (old, new) for old, new in zip(target_separators, form_separators) if old != new
    ]


def _holds_template(value):
    """Whether ``value`` holds a template at any depth of its own structure."""
    if isinstance(value, str):
        return False
    if isinstance(value, list):
        return any(_holds_template(item) for item in value)
    return True


def _selected_text(value, verse, keys_of=phase2.selected_keys):
    """The text of ``value`` along its selected parameters, as a note's target reads.

    ``keys_of(tmpl, verse)`` names the parameters read of each kept note or ketiv/qere
    template, by default phase2.selected_keys; phase5_readings.py's in-place test reads
    one side of each ketiv/qere template through it. The near-Aleppo dataset's rule-8 template, which phase 5
    writes, reads as MAM's notes write such marks, in square brackets.
    """
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        return "".join(_selected_text(item, verse, keys_of) for item in value)
    rule = phase2._RULES.get(value["tmpl_name"])
    action = rule.action if rule is not None else None
    if action in (phase2._KEEP_NOTE, phase2._KEEP_KQ):
        return "".join(
            _selected_text(value["tmpl_params"][key], verse, keys_of)
            for key in keys_of(value, verse)
        )
    if action == phase2._COLLAPSE_WORD:
        return value["tmpl_params"]["2"]
    if action == phase2._VERBATIM:
        return " "
    if action == phase2._CARRIERS:
        return phase2.carriers_text(value, verse)
    raise AssertionError(
        f"{verse}: {value['tmpl_name']!r} in a note's target, a template phase 2 "
        "does not keep"
    )


def _codex_forms(body, verse):
    """The forms a note body quotes from the codex, None for a clause agreeing with MAM.

    A clause quotes the codex where one of its sigla, as _parsed_clauses reads them,
    less any "!" or "?", is in _CODEX_SIGLA.
    """
    return [
        form
        for _, sigla, form in _parsed_clauses(body, verse)
        if any(siglum.rstrip("!?") in _CODEX_SIGLA for siglum in sigla)
    ]


def _parsed_clauses(body, verse):
    """Each clause of a note body that has an "=", as (head, sigla, form).

    A clause that opens with sigla and an "=" quotes the form after it, which runs
    to the first space, or is the whole of an angle-bracketed run, and _LIKE after
    the form introduces more sigla having it. Its head is the text before the "=".
    A clause that opens with "=" agrees with MAM: its head is empty, its sigla run
    to the first space or parenthesis, and its form is None.
    """
    parsed = []
    for clause in _clauses(body, verse):
        head, equals, rest = clause.partition("=")
        if not equals:
            continue
        if head:
            sigla = head.split(",")
            if rest.startswith("<"):
                form, _, after = rest[1:].partition(">")
            else:
                form, _, after = rest.partition(" ")
            after = after.strip()
            if after.startswith(_LIKE + " "):
                sigla += after[len(_LIKE) + 1 :].split(" ")[0].split(",")
        else:
            sigla = rest.split(" ")[0].split("(")[0].split(",")
            form = None
        parsed.append((head, sigla, form))
    return parsed


def _note_form_less_target(elements, index, headed, verse):
    """The codex form a note quotes for its target, less the target's text around
    the ketiv/qere template, which is element ``index`` of ``elements``.

    ``headed`` is the note's clauses headed א or א-כתיב, as (head, form). Raise
    unless there is exactly one, headed by one of those sigla alone, whose form
    has no "!" or "?"; unless the target's other elements are plain text, the form
    starting with the text before the template and ending with the text after it;
    and unless what remains has the letters of the template's ketiv, or at
    _KQ_FORM_WITH_QERE_LETTERS_VERSES of its qere.
    """
    if len(headed) != 1 or headed[0][0] not in _KQ_CODEX_HEADS:
        raise AssertionError(
            f"{verse}: the note has no one clause headed by א or א-כתיב alone"
        )
    form = headed[0][1]
    if "!" in form or "?" in form:
        raise AssertionError(f"{verse}: the note's codex form is bang- or doubt-marked")
    before, after = elements[:index], elements[index + 1 :]
    if not all(isinstance(text, str) for text in before + after):
        raise AssertionError(
            f"{verse}: a template beside the ketiv/qere template in a note's target"
        )
    before, after = "".join(before), "".join(after)
    if (
        len(form) < len(before) + len(after)
        or not form.startswith(before)
        or not form.endswith(after)
    ):
        raise AssertionError(
            f"{verse}: the note's codex form lacks the target's text around the "
            "ketiv/qere template"
        )
    remainder = form[len(before) : len(form) - len(after)]
    params = elements[index]["tmpl_params"]
    if verse in _KQ_FORM_WITH_QERE_LETTERS_VERSES:
        letters = params["2"]
    else:
        letters = params["1"]
    if _spelling(remainder) != _spelling(letters):
        raise AssertionError(
            f"{verse}: the note's codex form has letters other than those expected"
        )
    return remainder


def _prose_form(body, verse):
    """The one form a note body gives in prose: the one run in parentheses, among
    its clauses as _clauses reads them, that holds a mark. Any other number raises.
    """
    forms = [
        run
        for clause in _clauses(body, verse)
        for run in _PARENTHESIZED.findall(clause)
        if any(char in _MARKS for char in run)
    ]
    if len(forms) != 1:
        raise AssertionError(
            f"{verse}: {len(forms)} forms in parentheses in the note's prose, not 1"
        )
    return forms[0]


def _hataf_forms(body, verse):
    """The forms a note body quotes, for the hataf on a non-guttural.

    Return (quoting, agreeing). quoting has (head, forms) for each clause with
    sigla before its "=", head being the text before the "=" and forms what
    _quoted_forms reads after it. agreeing lists the forms in angle brackets
    anywhere in the clauses that open with "=".
    """
    quoting, agreeing = [], []
    for clause in _clauses(body, verse):
        if clause.startswith("="):
            agreeing += _ANGLE_RUN.findall(clause)
            continue
        head, equals, rest = clause.partition("=")
        if equals:
            quoting.append((head, _quoted_forms(rest)))
    return quoting, agreeing


def _quoted_forms(rest):
    """The forms a clause quotes after its "=".

    Where the text opens with "<", a run of forms in angle brackets joined by
    _OR. Otherwise its leading run of tokens, split at spaces, that carry a mark,
    with quotation marks stripped from each token, as one form. A clause can quote
    no form at all.

    The run of tokens stops at a token beginning with "<", after its quotation
    marks are stripped. Without the stop, Numbers
    25:18's clause citing א(ס) runs into the angle-bracketed comment that follows
    its bare form, because that comment's first token has marks, and phase 5 would
    meet a form holding a "<", which its replacement check refuses.
    """
    rest = rest.strip()
    if rest.startswith("<"):
        forms = []
        while rest.startswith("<"):
            form, _, rest = rest[1:].partition(">")
            forms.append(form)
            rest = rest.strip()
            if not rest.startswith(_OR + " "):
                break
            rest = rest[len(_OR) + 1 :].strip()
        return forms
    tokens = []
    for token in rest.split(" "):
        token = token.strip('"')
        if token.startswith("<") or not any(char in _MARKS for char in token):
            break
        tokens.append(token)
    return [" ".join(tokens)] if tokens else []


def _vowels_given(forms, place, spelling, index):
    """(vowel, marks) for each of ``forms`` whose letter aligned with a varika has one.

    The varika is on letter ``index`` of a note's target, whose letters are
    ``spelling`` with each final letter made non-final. ``place`` is the letters of
    that letter's atom and the letter's position in the atom. marks is the aligned
    letter's marks, and the vowel is what _hataf_vowel reads from them.
    """
    given = []
    for form in forms:
        marks = _aligned_marks(form, place, spelling, index)
        if marks is not None and _hataf_vowel(marks) is not None:
            given.append((_hataf_vowel(marks), marks))
    return given


def _aligned_marks(form, place, spelling, index):
    """The marks of the letter of ``form`` aligned with letter ``index`` of a target.

    ``place``, ``spelling`` and ``index`` are as _vowels_given has them. The aligned
    letter is the letter at the target letter's position in the first atom of the
    form whose letters are those of the target letter's atom; or, where the form
    has no such atom, the letter _only_match finds. None where there is neither.
    """
    atom_letters, position = place
    for atom in _atoms(form):
        if "".join(form[i] for i, _ in atom) == atom_letters:
            return "".join(form[i] for i in atom[position][1])
    letters = _letters_and_marks(form)
    matched = _only_match(
        spelling, "".join(letter for letter, _ in letters).translate(_NON_FINAL), index
    )
    return None if matched is None else letters[matched][1]


def _only_match(target, form, index):
    """The index of the letter of ``form`` that letter ``index`` of ``target``
    matches in every longest in-order matching of the letters of the two strings.

    None where some longest matching leaves that letter unmatched, or where it
    matches different letters of ``form`` in different longest matchings. Two
    tables of longest matchings, of the strings' beginnings and of their ends,
    decide this without enumerating the matchings, as _longest_matchings does.
    """
    rows, columns = len(target), len(form)
    # head[i][j]: the length of a longest matching of target[:i] with form[:j].
    head = [[0] * (columns + 1) for _ in range(rows + 1)]
    for i in range(rows):
        for j in range(columns):
            if target[i] == form[j]:
                head[i + 1][j + 1] = head[i][j] + 1
            else:
                head[i + 1][j + 1] = max(head[i][j + 1], head[i + 1][j])
    # tail[i][j]: the length of a longest matching of target[i:] with form[j:].
    tail = [[0] * (columns + 1) for _ in range(rows + 1)]
    for i in reversed(range(rows)):
        for j in reversed(range(columns)):
            if target[i] == form[j]:
                tail[i][j] = tail[i + 1][j + 1] + 1
            else:
                tail[i][j] = max(tail[i + 1][j], tail[i][j + 1])
    longest = head[rows][columns]
    without = max(head[index][j] + tail[index + 1][j] for j in range(columns + 1))
    if without == longest:
        return None
    matched = [
        j
        for j in range(columns)
        if target[index] == form[j]
        and head[index][j] + 1 + tail[index + 1][j + 1] == longest
    ]
    return matched[0] if len(matched) == 1 else None


def _hataf_vowel(marks):
    """The hataf a letter's marks give: a hataf patah, a hataf qamats or a hataf
    segol, or HIRIQ for a sheva with a hiriq, the codex's hataf hiriq as MAM's
    notes write it. None for any other marks."""
    for vowel in (HATAF_PATAH, HATAF_QAMATS, HATAF_SEGOL):
        if vowel in marks:
            return vowel
    if SHEVA in marks and HIRIQ in marks:
        return HIRIQ
    return None


def _inferred_hataf(letters, index):
    """The vowel the inference gives the varika on letter ``index`` of ``letters``.

    ``letters`` is a target's letters, as _letters_and_marks gives them, and the
    inference is MAM-basics' three rules, which the comment on _GUTTURALS states.
    None where the varika's letter is the target's last.
    """
    if index + 1 >= len(letters):
        return None
    letter, marks = letters[index + 1]
    vowel = next((mark for mark in marks if mark in _VOWELS), None)
    if letter in _GUTTURALS:
        if vowel in (QAMATS, QAMATS_QATAN):
            return HATAF_QAMATS
        if vowel == HIRIQ:
            return HIRIQ
    return HATAF_PATAH


def _stress_helpers_of(text, atom, verse):
    """Each stress helper of an atom, as (accent, index of its mark, its letter's
    position in the atom), ``accent`` being a key of _STRESS_HELPER_ACCENTS.

    An accent other than the zarqa has a stress helper where it is on two letters,
    one of them the letter where MAM has the accent itself, and the other copy is
    the stress helper. The zarqa has one where the atom has Unicode ZINOR on its last
    letter and Unicode ZARQA on an earlier one, the Unicode ZARQA being the stress
    helper. An atom with Unicode ZARQA and no Unicode ZINOR, the tsinnorit of a
    poetic verse, has none.

    Raise where an accent is on more than two letters, twice on one letter, or on two
    letters neither of which is the accent's own; where Unicode ZINOR is on two
    letters; and where Unicode ZARQA and Unicode ZINOR share an atom in any other
    arrangement, or in a poetic verse.
    """
    found = []
    for accent, (name, own) in _STRESS_HELPER_ACCENTS.items():
        copies = [
            (position, index)
            for position, (_, marks) in enumerate(atom)
            for index in marks
            if text[index] == accent
        ]
        positions = [position for position, _ in copies]
        if accent == UNICODE_ZINOR:
            helpers = [
                (position, index)
                for position, (_, marks) in enumerate(atom)
                for index in marks
                if text[index] == UNICODE_ZARQA
            ]
            if len(copies) > 1:
                raise AssertionError(f"{verse}: Unicode ZINOR on letters {positions}")
            if not copies or not helpers:
                continue
            if (
                _is_poetic(verse)
                or len(helpers) != 1
                or positions != [len(atom) - 1]
                or helpers[0][0] == len(atom) - 1
            ):
                raise AssertionError(
                    f"{verse}: Unicode ZARQA and Unicode ZINOR in an atom, not as a "
                    "prose zarqa and its stress helper"
                )
            found.append((accent, helpers[0][1], helpers[0][0]))
            continue
        if len(copies) < 2:
            continue
        own_position = own % len(atom)
        if (
            len(copies) != 2
            or len(set(positions)) != 2
            or own_position not in positions
        ):
            raise AssertionError(
                f"{verse}: a {name} on letters {positions} of an atom of {len(atom)} "
                "letters, not on its own letter and one other"
            )
        ((position, index),) = [pair for pair in copies if pair[0] != own_position]
        found.append((accent, index, position))
    return found


def _is_poetic(verse):
    """Whether ``verse``, named as main_build.py names it, is a poetic verse."""
    book, chapter, number = verse
    if book in _POETIC_BOOKS:
        return True
    first, last = _JOB_POETIC
    return book == _JOB and first <= (int(chapter), int(number)) <= last


def _has_doubling_phrase(body):
    """Whether the text of a note body, outside its templates, has a _DOUBLING_PHRASES."""
    items = body if isinstance(body, list) else [body]
    return any(
        phrase in item
        for item in items
        if isinstance(item, str)
        for phrase in _DOUBLING_PHRASES
    )


def _qualified_codex_sigla(head):
    """Codex sigla in ``head``, paired with their trailing ``!`` or ``?`` marks."""
    found = []
    for element in _split_outside_brackets(head):
        qualifier = element[len(element.rstrip("!?")) :]
        for siglum in _head_sigla(element.rstrip("!?")):
            if siglum in _STRESS_HELPER_CODEX_SIGLA:
                found.append((siglum, qualifier))
    return found


def _clause_sigla(clause):
    """The sigla of a note body's clause, as _head_sigla reads them.

    An agreeing clause's sigla follow its opening "=", up to the first space outside
    brackets. A differing clause's are its head, the text before its "=". A clause
    with no "=" has none.
    """
    if clause.startswith("="):
        rest = clause[1:]
        return _head_sigla(rest[: _first_space_outside_brackets(rest)])
    head, equals, _ = clause.partition("=")
    return _head_sigla(head) if equals else []


def _head_sigla(head):
    """The sigla of a clause's head, each less any "!" or "?".

    The head is split at commas outside brackets, and _TESTIMONY_LIST names several
    testimonies at once. A head with a space outside brackets is prose rather than
    a list of sigla, and has none. This reads a head as the census's
    nusach_aleppo_readings.py does.
    """
    head = head.strip()
    if _first_space_outside_brackets(head) < len(head):
        return []
    sigla = []
    for element in _split_outside_brackets(head):
        siglum = element.rstrip("!?")
        match = _TESTIMONY_LIST.match(siglum)
        if match is None:
            sigla.append(siglum)
        elif match.group(1).startswith(_PHOTOGRAPH):
            sigla.append(f"א({_PHOTOGRAPH})")
        else:
            sigla += [
                f"א({part.split('[')[0].strip()})"
                for part in match.group(1).split(",")
                if part.strip()
            ]
    return sigla


def _first_space_outside_brackets(text):
    """The index of the first space in ``text`` outside () and [], or its length."""
    depth = 0
    for index, char in enumerate(text):
        if char in "([":
            depth += 1
        elif char in ")]":
            depth -= 1
        elif char == " " and depth <= 0:
            return index
    return len(text)


def _split_outside_brackets(text):
    """``text`` split at its commas outside () and [], each part stripped, empty
    parts dropped."""
    parts, current, depth = [], "", 0
    for char in text:
        if char in "([":
            depth += 1
        elif char in ")]":
            depth -= 1
        if char == "," and depth <= 0:
            parts.append(current)
            current = ""
        else:
            current += char
    parts.append(current)
    return [part.strip() for part in parts if part.strip()]


def _atom_text(text, atom):
    """The text of ``atom``, from its first letter to its last letter or mark."""
    last_index, last_marks = atom[-1]
    return text[atom[0][0] : max([last_index] + last_marks) + 1]


def _matching_atom(form, letters):
    """The first atom of ``form`` whose letters are ``letters``, or else the first
    whose letters are those once each final letter is made non-final; None where
    there is neither."""
    atoms = _atoms(form)
    spelled = ["".join(form[index] for index, _ in atom) for atom in atoms]
    for atom, spelling in zip(atoms, spelled):
        if spelling == letters:
            return atom
    for atom, spelling in zip(atoms, spelled):
        if spelling.translate(_NON_FINAL) == letters.translate(_NON_FINAL):
            return atom
    return None


def _clauses(body, verse):
    """A note body's clauses, which _CLAUSE_SEPARATOR templates separate.

    A _LEGARMEH template is read as HEBREW PUNCTUATION PASEQ, the character phase 2
    writes for it in the body text, and a phase-2 paseq as that character followed
    by its space. A link is read as its display text, bold as its text, and a
    special-letter word as its ordinary spelling. Any other template raises: no
    policy that reads note bodies has been told how to read it.
    """
    clauses = [""]
    for item in body if isinstance(body, list) else [body]:
        if isinstance(item, str):
            clauses[-1] += item
            continue
        params = template_names.validate_current_plus_template(item)
        if item["tmpl_name"] == _CLAUSE_SEPARATOR:
            clauses.append("")
        elif item["tmpl_name"] == _LEGARMEH:
            clauses[-1] += PASEQ
        elif item["tmpl_name"] == _LINK:
            clauses[-1] += params["2"]
        elif item["tmpl_name"] == _INTERNAL_LINK:
            clauses[-1] += params["2"]
        elif item["tmpl_name"] == _BOLD:
            clauses[-1] += params["1"]
        elif item["tmpl_name"] == "מ:פסק":
            clauses[-1] += PASEQ + " "
        elif item["tmpl_name"] == phase2._SPECIAL_LETTER_WORD:
            clauses[-1] += params["2"]
        else:
            raise AssertionError(
                f"{verse}: {item['tmpl_name']!r} in the body of a note that a phase "
                "3 policy reads, a template no policy has been told how to read"
            )
    return [clause.strip() for clause in clauses]


def _lone_mark(text, marks, mark, verse, letter):
    """The index of the one ``mark`` among ``marks``; any other number raises."""
    found = [index for index in marks if text[index] == mark]
    if len(found) != 1:
        raise AssertionError(
            f"{verse}: {letter} has {len(found)} {unicodedata.name(mark)}, not 1"
        )
    return found[0]


def _note_opening(body):
    """A note body's text up to its first template; "" where there is no note."""
    if isinstance(body, str):
        return body
    if isinstance(body, list) and body and isinstance(body[0], str):
        return body[0]
    return ""


def _edited(text, edits):
    """``text`` with the character at each index of ``edits`` replaced by its value."""
    if not edits:
        return text
    return "".join(edits.get(index, char) for index, char in enumerate(text))
