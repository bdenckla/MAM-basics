"""Phase 5 of near-aleppo: the codex readings MAM's נוסח notes give.

The public build guide is ``doc/near-aleppo-build.md``.
Where a clause of a נוסח says that the codex has X where the dataset's target has Y,
the dataset takes X. MAM's notes supply the attributed codex forms. This module applies the
direct, undoubted clauses that quote one pointed form, and the differing clauses whose
head names שיטת-א, which rule 4 admits where the codex is lost. Where a clause gives
the codex's pointed ketiv at a כו״ק, קו״כ or מ:כו״ק מיוחד, it writes that pointed ketiv
into a parameter it adds to the template, phase2.POINTED_KETIV_PARAMETER, which is
then the template's selected parameter and so the body text, as rule 1 requires.

Which clauses. The build classifies every differing clause itself, with phase 3's
helpers, and imports no census code. Source sigla, quoting and doubt markers
determine the classification described below. A
clause differs where it has a non-empty head before its "=". A head with a space
outside brackets is prose, and a prose head whose last token, less any "!" or "?", is
a codex siglum is held pending, no decision having admitted its prose assertion as a
direct reading. That test comes first: Numbers 22:5's prose clause has a codex siglum
after a comma, which phase3._qualified_codex_sigla would otherwise find. Any other
head's codex sigla are rule 4's, as phase3._qualified_codex_sigla reads them, each with
its "!" or "?". A clause is pointed where its reading head, the angle-bracketed runs
where there are any and otherwise the text before its first " (", has a mark of
_POINTED. Its forms are those phase3._quoted_forms reads, with HEBREW POINT QAMATS QATAN
changed to HEBREW POINT QAMATS, so that phase 3's qamats-size policy holds in the
readings too. The classification tests, in order, give each clause one disposition
and reason: a "?" on a siglum, not applied and flagged by phase6_flags.py;
not pointed, not applied as a prose description; a first form ending in "?", not applied; a siglum א-כתיב or א-קרי,
pending, being a reading of a ketiv/qere plane; other than one form, pending; a "+",
"?", "[" or "]" in the form, pending; and otherwise an apply-candidate.

What becomes of an apply-candidate. The one in-place test, in_place below, which the
flags step uses too, compares the form, less any trailing "?", with the side of the
target that reading_side names: the ketiv side for a form headed א-כתיב and for the
readings _KETIV_LETTERS_READINGS names, the qere side for a form headed א-קרי, and the
target's selected text for every other form, which at a note of one of the two tables
it names may also be the named atoms of that text or that text less the paseq glyph
that ends it. A reading in place stays as it is; phases 2 and 3 put most of them there,
above all the hataf on a non-guttural and the revia mugrash. A reading not in place
replaces the whole of a plain target; at a note of _SUB_SPAN_READINGS, the named atoms
of it; and where the target is one kept מ:הערה-2, כו״ק, קו״כ or מ:כו״ק מיוחד, that
template's selected parameter, which in a ketiv/qere family must have the form's
letters. Any other shape raises, as does an apply-candidate that no outcome covers,
and so does a note with two readings that change its target.
A bang-marked reading is applied, and phase6_flags.py's bang rule flags it,
the reading being then in place. Three bang-marked readings have a configuration that
a phase 3 policy removes from MAM's text, each note saying so in words: they are applied
as quoted, _PHASE3_CONFIGURATION_READINGS names them, and no other applied reading may
have either configuration.

The readings of a ketiv/qere plane, and the pointed ketiv. The classification keeps
clauses headed א-כתיב or א-קרי pending; this
module then gives each an outcome. A form headed א-קרי must be in place on the qere
side, and nothing writes one. A form headed א-כתיב that is in place is so because
phase 3's ketiv/qere apparatus replaced the template by the note's form.
_PENDING_PLANE_READINGS names the forms that cannot be written as they stand, and
_ONE_SIDED_PLANE_READINGS those at a one-sided template, which remain pending. Every other form headed א-כתיב, and
each reading _KETIV_LETTERS_READINGS names, is written into the target's one ordinary
ketiv/qere template, a direct element beside plain text alone, as its pointed ketiv:
the form less the target's text before and after the template, cut as phase 3's
ketiv/qere apparatus cuts it, and adjusted where
_POINTED_KETIV_ADJUSTMENTS names the clause. Its letters must be the ketiv
parameter's as written, final forms included, and its spaces and maqafs the ketiv's,
except for a trailing maqaf, which must be the qere's, and the named adjustments. The
text outside the template must be the form's, except at Proverbs 3:30. It must hold
nothing phase 3 would change: no HEBREW POINT JUDEO-SPANISH VARIKA, HEBREW POINT
QAMATS QATAN, HEBREW MARK MASORA CIRCLE or ZERO WIDTH NON-JOINER, Job 38:12's
excepted, and neither configuration _PHASE3_CONFIGURATION_READINGS names. After
writing, the reading must be in place. At Isaiah 36:12 the pointed ketiv holds the near-Aleppo dataset's rule
8 template for marks written where no letter is, phase2.MARKS_WITHOUT_LETTER, which
the in-place test reads as MAM's notes write such marks, in square brackets.

The selected policies retain MAM's templates and original parameters, adding
``כתיב מנוקד`` for a pointed ketiv. _KETIV_LETTERS_READINGS names seven forms under
a plain א whose letters identify the ketiv side; Deuteronomy 32:13's form is already
in place through phase 3. At 2 Kings 14:7 the reading is written to the retained
קו״כ's selected qere parameter. Jeremiah 31:37 remains pending. Numbers 22:5 keeps
MAM's defective spelling, following the note's conclusion that the testimonies
conflict; phase6_flags.py gives the note a flagged-not-applied parameter holding the
א(ר) clause. Job 38:12 retains the form's ZERO WIDTH NON-JOINER between tav and he
to keep fonts from treating the he's patah as a furtive patah.

What stays for later work: the plane readings of _PENDING_PLANE_READINGS; those of
_ONE_SIDED_PLANE_READINGS and Jeremiah 31:37; the forms with exceptional punctuation,
the clauses with no form, the prose-led heads and the prose descriptions, which the
prose-description policy leaves without automatic treatment.

Subsequent sealed pointing imports supply retained ketiv/qere sites beyond this
note-derived set, without overwriting it.

The step runs after phase 3's policies and before phase6_mam_targets.py, which gives
every note whose target this step changes MAM's target, and phase6_flags.py.
"""

from collections import Counter
from collections import defaultdict
import re
from typing import NamedTuple

from near_aleppo import phase2_templates as phase2
from near_aleppo import phase3_policies as phase3

_NOTE = "נוסח"
_TARGET = "1"
_BODY = "2"


class Site(NamedTuple):
    """A clause a table names at its verse.

    ``note`` is the note's 1-based position among the נוסח that notes() finds in the
    verse, and ``clause`` the clause's 1-based position among the note's non-empty
    clauses, which is how the oracle numbers them.
    """

    note: int
    clause: int


# The oracle's pointed set: HEBREW ACCENT ETNAHTA to HEBREW POINT METEG, and six more
# marks. It leaves out the maqaf, the paseq glyph, the sof pasuq and the nun hafukha,
# each of which a prose description can have without quoting a form.
_POINTED = frozenset(chr(c) for c in range(0x0591, 0x05BE)) | {
    "\N{HEBREW POINT RAFE}",
    "\N{HEBREW POINT SHIN DOT}",
    "\N{HEBREW POINT SIN DOT}",
    "\N{HEBREW MARK UPPER DOT}",
    "\N{HEBREW MARK LOWER DOT}",
    "\N{HEBREW POINT QAMATS QATAN}",
}
# The sigla of the ketiv/qere planes, whose readings wait for the later ketiv/qere work.
_PLANE_SIGLA = frozenset({"א-כתיב", "א-קרי"})
# A form holding one of these is exceptional punctuation, not a plain reading.
_PUNCTUATION = "+?[]"

# The oracle's dispositions and reasons, in the words its golden prints.
_APPLY = "apply-candidate"
_DO_NOT_APPLY = "do-not-apply"
_PENDING = "policy-pending"
_DOUBT_SIGLUM = "doubt-siglum"
_PROSE_DESCRIPTION = "prose-description"
_DOUBT_FORM = "doubt-form"
_KETIV_QERE_PLANE = "ketiv-qere-plane"
_FORM_PUNCTUATION = "candidate-form-punctuation"
_SINGLE_POINTED_FORM = "single-pointed-form"

# The kept templates whose selected parameter a reading can be written into: the
# ordinary ketiv/qere families, phase2.POINTED_KETIV_FAMILIES, whose parameter 1 is the
# consonantal ketiv and whose parameter 2 is the pointed qere, selected until the
# template has a pointed ketiv, and the מ:הערה-2.
_KEPT_TARGET_FAMILIES = ("מ:הערה-2",) + phase2.POINTED_KETIV_FAMILIES
_QERE_WITHOUT_KETIV = "קרי ולא כתיב"
_KETIV_WITHOUT_QERE = "כתיב ולא קרי"

# The sides of a target that the in-place test compares a form with, as reading_side
# names them.
_SELECTED_SIDE = "the selected text"
_KETIV_SIDE = "the ketiv side"
_QERE_SIDE = "the qere side"
# The parameters each ketiv/qere family is read by on the ketiv side and on the qere
# side, where the family has that side. The ketiv side of an ordinary family is its
# pointed ketiv, phase2.POINTED_KETIV_PARAMETER, where it has one, and otherwise its
# consonantal ketiv; of a מ:קו״כ-אם-2 its parameter 1, MAM's pointed ketiv; of a
# כתיב ולא קרי its selected parameter, the ketiv, which is all it has; and a
# קרי ולא כתיב has nothing on the ketiv side. A כתיב ולא קרי has no qere side, and no
# clause headed א-קרי stands at one, so asking for it raises.
_SIDE_KEYS = {
    "כו״ק": {_KETIV_SIDE: ("1",), _QERE_SIDE: ("2",)},
    "קו״כ": {_KETIV_SIDE: ("1",), _QERE_SIDE: ("2",)},
    "מ:כו״ק מיוחד": {_KETIV_SIDE: ("1",), _QERE_SIDE: ("2",)},
    "מ:קו״כ-אם-2": {_KETIV_SIDE: ("1",), _QERE_SIDE: ("3",)},
    _QERE_WITHOUT_KETIV: {_KETIV_SIDE: (), _QERE_SIDE: ("2",)},
    _KETIV_WITHOUT_QERE: {_KETIV_SIDE: ("1",)},
}
# The Scripture-bearing parameters of each recognized ketiv/qere family. Phase 5
# validates these children directly and never searches arbitrary parameters for a
# nested template. The ordinary families may also have the pointed-ketiv parameter
# phase 5 adds; its exact string or near-Aleppo dataset's rule-8 shape is validated separately.
_KETIV_QERE_SCRIPTURE_KEYS = {
    "כו״ק": ("1", "2"),
    "קו״כ": ("1", "2"),
    "מ:כו״ק מיוחד": ("1", "2"),
    "מ:קו״כ-אם-2": ("1", "2", "3"),
    _QERE_WITHOUT_KETIV: ("1", "2"),
    _KETIV_WITHOUT_QERE: ("1", "2", "3"),
}
assert frozenset(_KETIV_QERE_SCRIPTURE_KEYS) == frozenset(_SIDE_KEYS)
assert all(
    phase2._RULES[name].action == phase2._KEEP_KQ for name in _KETIV_QERE_SCRIPTURE_KEYS
)
_KETIV_SIGLUM = "א-כתיב"
_QERE_SIGLUM = "א-קרי"

_MASORA_CIRCLE = "\N{HEBREW MARK MASORA CIRCLE}"
_ZERO_WIDTH_NON_JOINER = "\N{ZERO WIDTH NON-JOINER}"
# The near-Aleppo dataset's rule-8 carriers, in square brackets, then a space and the rest of a portion.
_CARRIERS_THEN_TEXT = re.compile(r"\[([^\]]*)\] (.+)")
# A rendering in single guillemets, as 2 Kings 18:27's note gives two.
_GUILLEMET_RUN = re.compile(
    "\N{SINGLE LEFT-POINTING ANGLE QUOTATION MARK}"
    "[^\N{SINGLE RIGHT-POINTING ANGLE QUOTATION MARK}]*"
    "\N{SINGLE RIGHT-POINTING ANGLE QUOTATION MARK}"
)
# What a pointed ketiv may not hold of the marks phase3._MARKS names: what phase 3
# would change, and the punctuation in the marks' range, which no ketiv parameter has.
# The ZERO WIDTH NON-JOINER, which only the reading _ZERO_WIDTH_NON_JOINER_READINGS
# names may hold, is checked apart.
_NOT_IN_POINTED_KETIV = {
    phase3.VARIKA: "HEBREW POINT JUDEO-SPANISH VARIKA",
    phase3.QAMATS_QATAN: "HEBREW POINT QAMATS QATAN",
    _MASORA_CIRCLE: "HEBREW MARK MASORA CIRCLE",
    phase3.PASEQ: "HEBREW PUNCTUATION PASEQ",
    "\N{HEBREW PUNCTUATION SOF PASUQ}": "HEBREW PUNCTUATION SOF PASUQ",
    "\N{HEBREW PUNCTUATION NUN HAFUKHA}": "HEBREW PUNCTUATION NUN HAFUKHA",
}

# In place though the form lacks the paseq glyph that ends the target. At these two the
# note's form quotes the atom without the legarmeh that follows it in MAM's text, whose
# HEBREW PUNCTUATION PASEQ phase 2 writes at the end of the target. The notes are about
# the hataf and the large nun, so the legarmeh stays.
_FORM_WITHOUT_PASEQ_READINGS = {
    ("D1-Psalms", "40", "13"): Site(1, 1),
    ("E2-Ruth", "3", "13"): Site(1, 2),
}
# The readings that replace named atoms of a plain target: the site, the first and the
# last atom replaced, and the target's atom count, atoms numbered from 1. At Deuteronomy
# 29:28 the note's form is the second of the target's four atoms with the pashta alone,
# the note saying that the codex has one pashta there, probably because of the crowding
# the extraordinary dots cause; this phase applies that explicit form. At
# Ezekiel 28:22 it is the second of the target's two atoms, the divine name.
_SUB_SPAN_READINGS = {
    ("A5-Deuter", "29", "28"): (Site(2, 2), 2, 2, 4),
    ("C3-Ezekiel", "28", "22"): (Site(1, 2), 2, 2, 2),
}
# At these a clause under an unqualified codex siglum quotes a form with the ketiv
# letters of the target's one כו״ק or קו״כ. The letters identify the ketiv side, so
# the form becomes the template's pointed ketiv. Deuteronomy 28:27's and 29:22's
# heads end in ל3-כתיב! and ל-כתיב!; the qualifier belongs to that siglum, as the
# census reads it, so neither reading is flagged. MAM-basics#290 asks whether these
# clauses should be headed א-כתיב on Wikisource.
# The table names seven forms. Deuteronomy 32:13's is already in place because
# phase 3's ketiv/qere apparatus replaces the template by the note's form, using
# the note's masorah note, which is not a qere note. That reading is therefore an
# ordinary apply-candidate, in place in the note's plain target.
_KETIV_LETTERS_FAMILIES = ("כו״ק", "קו״כ")
_KETIV_LETTERS_READINGS = {
    ("A5-Deuter", "28", "27"): Site(1, 2),
    ("A5-Deuter", "29", "22"): Site(2, 3),
    ('BC-Kings מל"ב', "4", "3"): Site(1, 1),
    ("D2-Proverbs", "22", "8"): Site(1, 1),
    ("D2-Proverbs", "22", "11"): Site(1, 1),
    ("D2-Proverbs", "22", "14"): Site(1, 1),
    ('FC-Chronicles דה"א', "18", "10"): Site(1, 1),
}
# Jeremiah 31:37 remains pending: its form stops at the clause's "[]", the codex's
# unpointed space for the קרי ולא כתיב. This is a one-sided ketiv/qere case.
_QERE_WITHOUT_KETIV_READINGS = {("C2-Jeremiah", "31", "37"): Site(1, 2)}

# The pointed ketiv written with a named adjustment. At 2 Samuel 5:2 and 21:12 the form's two
# HEBREW MARK MASORA CIRCLE go, rule 10 excluding masorah circles from the dataset, and
# the in-place test compares the form less them. At Isaiah 44:24 the form's maqaf stays
# where MAM's ketiv, מי אתי, has a space, the clause's parenthetical saying that the
# maqaf shows the two written atoms read together. At Isaiah 36:12 the form opens with
# the codex's pointing of the qere's first word, in square brackets on two alefs, which
# the clause says stands in the margin at the line's end, in a space of two letters: it
# is written as the near-Aleppo dataset's rule-8 template, phase2.MARKS_WITHOUT_LETTER, then a space and the
# pointed ketiv, rule 8's first use in the dataset. At Proverbs 3:30 the bang-marked
# form has a space where the target has a maqaf before the template, its parenthetical
# saying that the maqaf is missing, and the target's maqaf becomes a space: the maqaf
# policy leaves that ketiv-plane clause to this phase.
_WITHOUT_MASORA_CIRCLES = "the form's two HEBREW MARK MASORA CIRCLE removed"
_MAQAF_FOR_KETIV_SPACE = "the form's maqaf kept where the ketiv has a space"
_CARRIERS_FIRST = "the form's bracketed marks written as rule 8's template"
_SPACE_FOR_MAQAF_BEFORE = "the maqaf before the template made a space"
_POINTED_KETIV_ADJUSTMENTS = {
    ('BA-Samuel שמ"ב', "5", "2"): (Site(1, 1), _WITHOUT_MASORA_CIRCLES),
    ('BA-Samuel שמ"ב', "21", "12"): (Site(1, 1), _WITHOUT_MASORA_CIRCLES),
    ("C1-Isaiah", "36", "12"): (Site(2, 1), _CARRIERS_FIRST),
    ("C1-Isaiah", "44", "24"): (Site(1, 1), _MAQAF_FOR_KETIV_SPACE),
    ("D2-Proverbs", "3", "30"): (Site(1, 2), _SPACE_FOR_MAQAF_BEFORE),
}
# The one pointed ketiv holding a ZERO WIDTH NON-JOINER, which MAM-parsed-plus has
# only in this note's body. The character is retained between tav and he to keep
# fonts from treating the he's patah as a furtive patah.
_ZERO_WIDTH_NON_JOINER_READINGS = {("D3-Job", "38", "12"): Site(1, 1)}
# Named pending forms that cannot be written as they stand. At 2 Kings 18:27 the clause gives two renderings in single
# guillemets, the first with a "+" gloss and a bracketed alef, the second with marks on
# no letter, and which marks the yod has is not settled mechanically. At Jeremiah 48:20
# the form is the second of the ketiv's two words alone, so the note gives no pointed
# ketiv for the first. At 1 Chronicles 9:4 the form has no separator after it, while
# MAM's qere ends in a maqaf and the verse's next atom follows the note with no space;
# the maqaf policy deferred the clause for the same question.
_TWO_RENDERINGS = "two renderings in single guillemets"
_SECOND_WORD_ALONE = "the second of the ketiv's two words alone"
_NO_SEPARATOR_AFTER = "no separator after the form, where the qere ends in a maqaf"
_PENDING_PLANE_READINGS = {
    ('BC-Kings מל"ב', "18", "27"): (Site(2, 2), _TWO_RENDERINGS),
    ("C2-Jeremiah", "48", "20"): (Site(1, 1), _SECOND_WORD_ALONE),
    ('FC-Chronicles דה"א', "9", "4"): (Site(1, 1), _NO_SEPARATOR_AFTER),
}
# Plane readings at one-sided templates remain pending.
_ONE_SIDED_PLANE_READINGS = {
    ('BC-Kings מל"ב', "5", "18"): (Site(1, 2), _KETIV_WITHOUT_QERE),
    ("C2-Jeremiah", "50", "29"): (Site(1, 1), _QERE_WITHOUT_KETIV),
}
# The only plane readings whose selected target has no ketiv/qere template when phase
# 5 receives it. At each exact site, phase 3's ketiv/qere apparatus replaced the
# direct template by the note's form. A zero-template target anywhere else raises.
_PHASE3_REPLACED_PLANE_READINGS = {
    ("D1-Psalms", "89", "29"): Site(1, 2),
    ('FC-Chronicles דה"ב', "25", "17"): Site(1, 2),
    ('FC-Chronicles דה"ב', "34", "22"): Site(1, 2),
}
# Not applied, and flagged by phase6_flags.py, following the note's conclusion.
# Numbers 22:5's א(ר) clause gives the plene spelling; the note's agreeing clause cites
# א(ו) for MAM's defective one; and its prose clause calls the codex's testimonies
# contradictory and prefers א(ו)'s explicit testimony to א(ר)'s testimony from silence.
NOT_APPLIED_READINGS = {("A4-Numbers", "22", "5"): Site(1, 2)}
_SILENT_TESTIMONY = "א(ר)"
_EXPLICIT_TESTIMONY = "א(ו)"

# The three bang-marked readings with a configuration that a phase 3 policy removes
# from MAM's text, each note saying so in words. At Psalms 11:1 and 56:5 the codex has
# the ole and the yored on one letter, which the ole on the yored's letter removes; at
# Ezekiel 28:22 it has the divine name with the vowels of the Adonai reading and a
# holam on the first he, which the divine-name holam removes. They are applied as quoted, and phase6_flags.py flags them. An applied
# reading with either configuration at a site this table does not name raises.
_OLE_AND_YORED = "the ole and the yored on one letter"
_ADONAI_READING_HOLAM = "a holam on the first he of the divine name's Adonai reading"
_PHASE3_CONFIGURATION_READINGS = {
    ("C3-Ezekiel", "28", "22"): (Site(1, 2), _ADONAI_READING_HOLAM),
    ("D1-Psalms", "11", "1"): (Site(1, 2), _OLE_AND_YORED),
    ("D1-Psalms", "56", "5"): (Site(1, 1), _OLE_AND_YORED),
}

# Differing clauses whose head names שיטת-א are admitted only where the codex is
# lost. The table identifies thirteen clauses explicitly, each at a lost verse. MAM-parsed-plus supplies the Scripture
# and notes; the public census checks extantness independently.
# In place: phase 3 removes revia mugrash's revia at nine Psalms verses and restores
# hataf on non-gutturals at Psalms 17:14 and 18:7. Not applied: Leviticus 10:4,
# where the dataset follows the note's א(ס) testimony instead, through phase 3's
# _TELISHA_GEDOLA_WORDS. Applied: Song of Songs 8:4, whose clause gives hataf patah
# on the first resh where the target has sheva; the same note's agreeing clause
# also names שיטת-א for the merkha, which the form has.
_SHITAT_ALEF = "שיטת-א"
_SHITAT_ALEF_IN_PLACE = "in place"
_SHITAT_ALEF_NOT_APPLIED = "not applied"
_SHITAT_ALEF_APPLIED = "applied"
_SHITAT_ALEF_READINGS = {
    ("A3-Levit", "10", "4"): _SHITAT_ALEF_NOT_APPLIED,
    ("D1-Psalms", "16", "1"): _SHITAT_ALEF_IN_PLACE,
    ("D1-Psalms", "17", "6"): _SHITAT_ALEF_IN_PLACE,
    ("D1-Psalms", "17", "10"): _SHITAT_ALEF_IN_PLACE,
    ("D1-Psalms", "17", "14"): _SHITAT_ALEF_IN_PLACE,
    ("D1-Psalms", "18", "7"): _SHITAT_ALEF_IN_PLACE,
    ("D1-Psalms", "18", "12"): _SHITAT_ALEF_IN_PLACE,
    ("D1-Psalms", "18", "31"): _SHITAT_ALEF_IN_PLACE,
    ("D1-Psalms", "18", "32"): _SHITAT_ALEF_IN_PLACE,
    ("D1-Psalms", "20", "9"): _SHITAT_ALEF_IN_PLACE,
    ("D1-Psalms", "22", "21"): _SHITAT_ALEF_IN_PLACE,
    ("D1-Psalms", "23", "3"): _SHITAT_ALEF_IN_PLACE,
    ("E1-Song of Songs", "8", "4"): _SHITAT_ALEF_APPLIED,
}

# Every verse table, by the name its use is counted under. Each site a table names must
# exist, have the shape the table assumes, and be used once.
_TABLES = {
    "_FORM_WITHOUT_PASEQ_READINGS": _FORM_WITHOUT_PASEQ_READINGS,
    "_SUB_SPAN_READINGS": _SUB_SPAN_READINGS,
    "_KETIV_LETTERS_READINGS": _KETIV_LETTERS_READINGS,
    "_QERE_WITHOUT_KETIV_READINGS": _QERE_WITHOUT_KETIV_READINGS,
    "NOT_APPLIED_READINGS": NOT_APPLIED_READINGS,
    "_PHASE3_CONFIGURATION_READINGS": _PHASE3_CONFIGURATION_READINGS,
    "_SHITAT_ALEF_READINGS": _SHITAT_ALEF_READINGS,
    "_POINTED_KETIV_ADJUSTMENTS": _POINTED_KETIV_ADJUSTMENTS,
    "_ZERO_WIDTH_NON_JOINER_READINGS": _ZERO_WIDTH_NON_JOINER_READINGS,
    "_PENDING_PLANE_READINGS": _PENDING_PLANE_READINGS,
    "_ONE_SIDED_PLANE_READINGS": _ONE_SIDED_PLANE_READINGS,
    "_PHASE3_REPLACED_PLANE_READINGS": _PHASE3_REPLACED_PLANE_READINGS,
}

# How the in-place test finds a form in place.
_AS_SELECTED = "the target's selected text"
_ON_ITS_SIDE = "the target's ketiv side or qere side"
_WITHOUT_PASEQ = "the target's selected text less the paseq glyph that ends it"
_NAMED_ATOMS = "the named atoms of the target's selected text"

# The tallies. A reason's label is _reason_label's, and a bang-marked clause is counted
# a second time under its label with _BANG added.
_BANG = ", bang-marked"
_NOTES = "codex readings: notes walked"
_EMPTY_CLAUSES = "codex readings: empty clauses in note bodies"
_ELEMENTS = "codex readings: direct codex siglum elements"
_CLAUSES = "codex readings: direct differing clauses"
_VERSES = "codex readings: verses with a direct differing clause"
_PROSE_LED = "codex readings: prose-led heads ending in a codex siglum, held pending"
_IN_PLACE = "codex readings: apply-candidate already in place"
_IN_PLACE_WITHOUT_PASEQ = (
    "codex readings: apply-candidate in place, its form lacking the paseq glyph that "
    "ends the target"
)
_APPLIED_WHOLE = (
    "codex readings: applied, the form replacing the whole of a plain target"
)
_APPLIED_ATOMS = (
    "codex readings: applied, the form replacing named atoms of a plain target"
)
_APPLIED_KEPT = (
    "codex readings: applied, the form written into the selected parameter of the one "
    "kept template that is the target"
)
_PENDING_QERE_WITHOUT_KETIV = (
    "codex readings: pending, the form stopping at the codex's space for a qere "
    "without ketiv"
)
_NOT_APPLIED = "codex readings: not applied, and flagged"
_TARGETS_CHANGED = "codex readings: note targets changed"
_CONFIGURATIONS = (
    "codex readings: applied readings with a configuration a phase 3 policy removes"
)
_SHITAT_ALEF_CLAUSES = "codex readings: differing clauses whose head names שיטת-א"
_SHITAT_ALEF_PROSE = (
    "codex readings: differing clauses whose head names שיטת-א, the head being prose"
)
_SHITAT_ALEF_OUTCOMES = {
    _SHITAT_ALEF_IN_PLACE: "codex readings: שיטת-א reading already in place",
    _SHITAT_ALEF_NOT_APPLIED: "codex readings: שיטת-א reading not applied",
    _SHITAT_ALEF_APPLIED: (
        "codex readings: שיטת-א reading applied, the whole of a plain target"
    ),
}
# Outcomes for readings of a ketiv/qere plane and of _KETIV_LETTERS_READINGS.
_PLANE_IN_QERE = "codex readings: ketiv/qere plane reading in place in a qere parameter"
_PLANE_IN_PLACE_BY_PHASE_3 = (
    "codex readings: ketiv/qere plane reading in place through phase 3's ketiv/qere "
    "apparatus"
)
_WRITTEN_AS_IT_STANDS = "codex readings: pointed ketiv written as the form stands"
_WRITTEN_ADJUSTED = "codex readings: pointed ketiv written with a named adjustment"
_PLANE_PENDING = "codex readings: ketiv/qere plane reading pending by name"
_PLANE_ONE_SIDED = (
    "codex readings: ketiv/qere plane reading at a one-sided template, left for later "
    "work"
)
# Pointed ketivs ending in the qere's trailing maqaf, retained as part of the pointing.
_TRAILING_MAQAF = "codex readings: pointed ketiv ending in the qere's trailing maqaf"

# The build records these counts and site lists in
# in/near-aleppo/build-populations.json, pinning none of them, so that a changed
# disposition count or site list shows in that file's diff.
#
# The build classifies direct source clauses and derives their outcomes: forms
# already in place, forms written to whole targets or named atoms, forms written
# to selected parameters or added pointed-ketiv parameters, and named pending or
# not-applied forms. It records bang-marked outcomes, named adjustments and
# trailing maqafs separately. Deuteronomy 32:13's form is already in place through
# phase 3's apparatus and is an ordinary apply-candidate, not an added pointing.
# The shitat-Alef table is checked separately against current source clauses.
#
# An empty clause takes no number: a Site's clause counts the note's non-empty
# clauses only, as the oracle numbers them.


class _Clause(NamedTuple):
    """A differing clause phase 5 may apply: its site, sigla and forms."""

    site: Site
    sigla: tuple
    rest: str
    forms: tuple
    bang: bool


class _DirectKetivQereTarget(NamedTuple):
    """One validated direct ketiv/qere template and its surrounding plain text."""

    template: dict
    index: int
    before: str
    after: str


class Readings:
    """Applies phase 5's codex readings verse by verse and tallies what it did."""

    def __init__(self):
        self.counts = Counter()
        self.sites = defaultdict(list)
        # How many times each table was used in the current verse.
        self._uses = Counter()

    def apply_e_cell(self, cell, verse):
        """Apply one E cell's codex readings, in place, and return the cell.

        ``cell`` is the E cell phase 3 returns, and ``verse`` names the verse as
        main_build.py does.
        """
        self._uses = Counter()
        found = notes(cell, verse)
        self.counts[_NOTES] += len(found)
        direct = 0
        for number, note in enumerate(found, 1):
            direct += self._note(note, number, verse)
        if direct:
            self.counts[_VERSES] += 1
        for name, table in _TABLES.items():
            if verse in table and self._uses[name] != 1:
                raise AssertionError(
                    f"{verse}: named in {name}, which was used {self._uses[name]} "
                    "times at the verse, not 1"
                )
        return cell

    def _note(self, note, number, verse):
        """Classify one note's differing clauses, apply its reading, and return the
        number of its direct differing clauses."""
        params = note["tmpl_params"]
        candidates = []
        plane = []
        shitat_alef = []
        direct = 0
        position = 0
        for text in phase3._clauses(params[_BODY], verse):
            if not text:
                self._tally(_EMPTY_CLAUSES, verse)
                continue
            position += 1
            head, equals, rest = text.partition("=")
            if not equals or not head:
                continue
            stripped = head.strip()
            prose = phase3._first_space_outside_brackets(stripped) < len(stripped)
            codex_led = (
                prose
                and stripped.split()[-1].rstrip("!?")
                in phase3._STRESS_HELPER_CODEX_SIGLA
            )
            sigla = () if prose else tuple(phase3._qualified_codex_sigla(head))
            if _SHITAT_ALEF in head:
                if codex_led or sigla:
                    raise AssertionError(
                        f"{verse}: a clause whose head names שיטת-א and cites the "
                        "codex too, which no policy says how to read"
                    )
                shitat_alef.append((Site(number, position), stripped, rest))
                continue
            if codex_led:
                self._tally(_PROSE_LED)
                continue
            if not sigla:
                continue
            direct += 1
            disposition, reason, clause = _classified(
                Site(number, position), sigla, rest, verse
            )
            self.counts[_ELEMENTS] += len(sigla)
            self._tally(_CLAUSES)
            self._tally(_reason_label(disposition, reason), bang=clause.bang)
            if disposition == _APPLY:
                candidates.append(clause)
            elif reason == _KETIV_QERE_PLANE:
                plane.append(clause)
        if len(candidates) + len(shitat_alef) > 1:
            raise AssertionError(
                f"{verse}: note {number} has {len(candidates)} apply-candidates and "
                f"{len(shitat_alef)} differing שיטת-א clauses; no policy says which "
                "applies"
            )
        changed = self.counts[_TARGETS_CHANGED]
        for clause in candidates:
            self._candidate(clause, note, verse)
        for clause in plane:
            self._plane(clause, note, verse)
        for site, head, rest in shitat_alef:
            self._shitat_alef(site, head, rest, note, verse)
        if self.counts[_TARGETS_CHANGED] - changed > 1:
            raise AssertionError(
                f"{verse}: note {number} has more than one reading that changes its "
                "target; no policy says which applies"
            )
        return direct

    def _candidate(self, clause, note, verse):
        """Decide and carry out what becomes of one apply-candidate."""
        target = note["tmpl_params"][_TARGET]
        form = clause.forms[0]
        if _KETIV_LETTERS_READINGS.get(verse) == clause.site:
            self._uses["_KETIV_LETTERS_READINGS"] += 1
            direct_target = _direct_ketiv_qere_target(target, verse, clause.site)
            if direct_target is None:
                raise AssertionError(
                    f"{verse}: a ketiv-side reading to write at a target phase 3 "
                    "replaced"
                )
            _check_ketiv_letters(form, target, verse)
            if in_place(form, target, verse, clause.site.note, _KETIV_SIDE):
                raise AssertionError(
                    f"{verse}: a reading _KETIV_LETTERS_READINGS names, in place "
                    "already on the ketiv side"
                )
            outcome = self._write_pointed_ketiv(clause, note, verse, direct_target)
        elif _QERE_WITHOUT_KETIV_READINGS.get(verse) == clause.site:
            self._uses["_QERE_WITHOUT_KETIV_READINGS"] += 1
            _check_qere_without_ketiv(clause, target, verse)
            outcome = _PENDING_QERE_WITHOUT_KETIV
        elif NOT_APPLIED_READINGS.get(verse) == clause.site:
            self._uses["NOT_APPLIED_READINGS"] += 1
            _check_not_applied(clause, note, verse)
            outcome = _NOT_APPLIED
        else:
            kind = _in_place_kind(form, target, verse, clause.site.note, _SELECTED_SIDE)
            if kind == _AS_SELECTED:
                outcome = _IN_PLACE
            elif kind == _WITHOUT_PASEQ:
                if _FORM_WITHOUT_PASEQ_READINGS[verse] != clause.site:
                    raise AssertionError(
                        f"{verse}: clause {clause.site.clause} of note "
                        f"{clause.site.note} lacks the target's paseq glyph, and the "
                        "table names another clause"
                    )
                self._uses["_FORM_WITHOUT_PASEQ_READINGS"] += 1
                outcome = _IN_PLACE_WITHOUT_PASEQ
            elif kind == _NAMED_ATOMS:
                raise AssertionError(
                    f"{verse}: a reading its table says replaces named atoms is in "
                    "place already"
                )
            else:
                outcome = self._apply(form, note, clause.site, verse)
                self._check_configurations(form, clause.site, verse)
                self._tally(_TARGETS_CHANGED, bang=clause.bang)
        self._tally(outcome, None if outcome == _IN_PLACE else verse, bang=clause.bang)

    def _shitat_alef(self, site, head, rest, note, verse):
        """Check, and apply where its table says so, a differing שיטת-א clause."""
        outcome = _SHITAT_ALEF_READINGS.get(verse)
        if outcome is None:
            raise AssertionError(
                f"{verse}: a differing clause whose head names שיטת-א, at a verse the "
                "table does not name"
            )
        self._uses["_SHITAT_ALEF_READINGS"] += 1
        self._tally(_SHITAT_ALEF_CLAUSES)
        if phase3._first_space_outside_brackets(head) < len(head):
            self._tally(_SHITAT_ALEF_PROSE)
        if not head.endswith(_SHITAT_ALEF):
            raise AssertionError(
                f"{verse}: a שיטת-א clause whose head does not end in an unqualified "
                "שיטת-א"
            )
        disposition, _, forms = _disposition((), rest)
        if disposition != _APPLY:
            raise AssertionError(
                f"{verse}: a שיטת-א clause that does not quote one plain pointed form"
            )
        form = forms[0]
        placed = in_place(
            form, note["tmpl_params"][_TARGET], verse, site.note, _SELECTED_SIDE
        )
        if outcome == _SHITAT_ALEF_IN_PLACE and not placed:
            raise AssertionError(
                f"{verse}: a שיטת-א reading its table says is in place"
            )
        if outcome != _SHITAT_ALEF_IN_PLACE and placed:
            raise AssertionError(
                f"{verse}: a שיטת-א reading in place, which its table says is not"
            )
        if outcome == _SHITAT_ALEF_APPLIED:
            if self._apply(form, note, site, verse) != _APPLIED_WHOLE:
                raise AssertionError(
                    f"{verse}: a שיטת-א reading whose target is not plain text"
                )
            self._check_configurations(form, site, verse)
            self._tally(_TARGETS_CHANGED)
        self._tally(_SHITAT_ALEF_OUTCOMES[outcome], verse)

    def _apply(self, form, note, site, verse):
        """Write ``form`` into the target of ``note``, in place; return how.

        The shapes are closed: a plain target, of which the form replaces the whole or,
        at a site of _SUB_SPAN_READINGS, the named atoms; and one kept template of
        _KEPT_TARGET_FAMILIES, whose selected parameter the form replaces, the form
        having the qere's letters in a ketiv/qere family. Any other shape raises.
        """
        params = note["tmpl_params"]
        target = params[_TARGET]
        sub_span = _SUB_SPAN_READINGS.get(verse)
        if sub_span is not None and sub_span[0] == site:
            self._uses["_SUB_SPAN_READINGS"] += 1
            if not isinstance(target, str):
                raise AssertionError(
                    f"{verse}: a sub-span reading whose target is not plain text"
                )
            start, end = _named_span(target, sub_span, verse)
            if phase3._spelling(form) != phase3._spelling(target[start:end]):
                raise AssertionError(
                    f"{verse}: a sub-span reading whose letters are not the named "
                    "atoms'"
                )
            _check_replacement(form, target[start:end], verse)
            params[_TARGET] = target[:start] + form + target[end:]
            kind = _APPLIED_ATOMS
        elif isinstance(target, str):
            _check_replacement(form, target, verse)
            params[_TARGET] = form
            kind = _APPLIED_WHOLE
        elif isinstance(target, dict) and target["tmpl_name"] in _KEPT_TARGET_FAMILIES:
            name = target["tmpl_name"]
            (key,) = phase2.selected_keys(target, verse)
            value = target["tmpl_params"][key]
            if not isinstance(value, str):
                raise AssertionError(
                    f"{verse}: a reading for a {name} whose selected parameter is not "
                    "plain text"
                )
            if name in phase2.POINTED_KETIV_FAMILIES:
                if key == phase2.POINTED_KETIV_PARAMETER:
                    raise AssertionError(
                        f"{verse}: a reading for the qere of a {name} whose pointed "
                        "ketiv is its selected parameter"
                    )
                letters = phase3._spelling(form)
                if letters == phase3._spelling(target["tmpl_params"]["1"]):
                    raise AssertionError(
                        f"{verse}: a reading with the ketiv's letters at a {name}, at "
                        "a site _KETIV_LETTERS_READINGS does not name"
                    )
                if letters != phase3._spelling(value):
                    raise AssertionError(
                        f"{verse}: a reading at a {name} with the letters of neither "
                        "its ketiv nor its qere"
                    )
            _check_replacement(form, value, verse)
            target["tmpl_params"][key] = form
            kind = _APPLIED_KEPT
        else:
            raise AssertionError(
                f"{verse}: a codex reading whose target has no shape phase 5 writes a "
                "reading into"
            )
        if not in_place(form, params[_TARGET], verse, site.note, _SELECTED_SIDE):
            raise AssertionError(f"{verse}: an applied reading is not in place")
        return kind

    def _plane(self, clause, note, verse):
        """Decide and carry out what becomes of one reading of a ketiv/qere plane.

        The selected target is validated as one direct ketiv/qere template beside
        plain text alone, or as one of the three exact targets whose template phase 3
        replaced. A table's site is then checked for the shape its table assumes.
        Otherwise a form headed א-קרי must be in place on the qere side of the direct
        template; an explicitly named phase-3 replacement must be in place on the
        ketiv side; and every other form headed א-כתיב is written as the direct
        template's pointed ketiv.
        """
        target = note["tmpl_params"][_TARGET]
        side = reading_side(clause.sigla, verse, clause.site)
        direct_target = _direct_ketiv_qere_target(target, verse, clause.site)
        pending = _PENDING_PLANE_READINGS.get(verse)
        one_sided = _ONE_SIDED_PLANE_READINGS.get(verse)
        if pending is not None and pending[0] == clause.site:
            self._uses["_PENDING_PLANE_READINGS"] += 1
            _check_pending_plane(clause, target, direct_target, pending[1], side, verse)
            outcome = _PLANE_PENDING
        elif one_sided is not None and one_sided[0] == clause.site:
            self._uses["_ONE_SIDED_PLANE_READINGS"] += 1
            _check_one_sided_plane(
                clause, target, direct_target, one_sided[1], side, verse
            )
            outcome = _PLANE_ONE_SIDED
        else:
            if len(clause.forms) != 1:
                raise AssertionError(
                    f"{verse}: a ketiv/qere plane clause with {len(clause.forms)} "
                    "forms, not 1, at a site no table names"
                )
            placed = in_place(clause.forms[0], target, verse, clause.site.note, side)
            if direct_target is None:
                self._uses["_PHASE3_REPLACED_PLANE_READINGS"] += 1
                if side != _KETIV_SIDE or not placed:
                    raise AssertionError(
                        f"{verse}: an explicitly named phase-3 replacement that is "
                        "not in place on the ketiv side"
                    )
                outcome = _PLANE_IN_PLACE_BY_PHASE_3
            elif side == _QERE_SIDE:
                if not placed:
                    raise AssertionError(
                        f"{verse}: a reading headed א-קרי that is not in place in a "
                        "direct ketiv/qere template's qere, which no policy writes"
                    )
                outcome = _PLANE_IN_QERE
            elif placed:
                raise AssertionError(
                    f"{verse}: a reading headed א-כתיב in place while its direct "
                    "ketiv/qere template remains"
                )
            else:
                outcome = self._write_pointed_ketiv(clause, note, verse, direct_target)
        self._tally(outcome, verse, bang=clause.bang)

    def _write_pointed_ketiv(self, clause, note, verse, direct_target):
        """Write the pointed ketiv that ``clause`` quotes into its note's target, in
        place, and return the outcome's label.

        ``direct_target`` is the selected target validated by
        _direct_ketiv_qere_target. Its template is one of
        phase2.POINTED_KETIV_FAMILIES, whose parameters 1 and 2 are plain text and
        which has no pointed ketiv yet. The clause's one form, less the target's text
        before and after the template, as phase3._note_form_less_target cuts it, and
        adjusted as _POINTED_KETIV_ADJUSTMENTS names, becomes
        phase2.POINTED_KETIV_PARAMETER, after MAM's parameters; at Proverbs 3:30 the
        target's text before the template changes too. _check_pointed_ketiv checks
        what is written.
        """
        params = note["tmpl_params"]
        template, _, before, after = direct_target
        name = template["tmpl_name"]
        if name not in phase2.POINTED_KETIV_FAMILIES:
            raise AssertionError(
                f"{verse}: a pointed ketiv to write at {name!r}, not כו״ק, קו״כ or "
                "מ:כו״ק מיוחד"
            )
        template_params = template["tmpl_params"]
        ketiv, qere = template_params["1"], template_params["2"]
        if phase2.POINTED_KETIV_PARAMETER in template_params:
            raise AssertionError(f"{verse}: a template with a pointed ketiv already")
        if not isinstance(ketiv, str) or not isinstance(qere, str):
            raise AssertionError(
                f"{verse}: a pointed ketiv to write at a template whose ketiv or qere "
                "is not plain text"
            )
        if len(clause.forms) != 1:
            raise AssertionError(
                f"{verse}: a pointed ketiv to write from {len(clause.forms)} forms"
            )
        (form,) = clause.forms
        original_before = before
        adjustment = None
        named = _POINTED_KETIV_ADJUSTMENTS.get(verse)
        if named is not None and named[0] == clause.site:
            self._uses["_POINTED_KETIV_ADJUSTMENTS"] += 1
            adjustment = named[1]
        if adjustment == _SPACE_FOR_MAQAF_BEFORE:
            if not before.endswith(phase3.MAQAF):
                raise AssertionError(
                    f"{verse}: no maqaf before the template to make a space"
                )
            before = before[:-1] + " "
        portion = _portion(form, before, after, verse)
        carriers = None
        if adjustment == _WITHOUT_MASORA_CIRCLES:
            if portion.count(_MASORA_CIRCLE) != 2:
                raise AssertionError(
                    f"{verse}: a form with {portion.count(_MASORA_CIRCLE)} HEBREW MARK "
                    "MASORA CIRCLE, where the table assumes 2"
                )
            portion = portion.replace(_MASORA_CIRCLE, "")
        elif adjustment == _CARRIERS_FIRST:
            match = _CARRIERS_THEN_TEXT.fullmatch(portion)
            if match is None:
                raise AssertionError(
                    f"{verse}: a form that does not open with bracketed marks and a "
                    "space, where the table assumes it does"
                )
            carriers, portion = match.groups()
        trailing = self._check_pointed_ketiv(
            portion, carriers, ketiv, qere, adjustment, clause.site, verse
        )
        value = portion
        if carriers is not None:
            value = [phase2.marks_without_letter(carriers, verse), " " + portion]
        template_params[phase2.POINTED_KETIV_PARAMETER] = value
        if before != original_before:
            params[_TARGET] = phase2._simplify(
                phase2._merge_strings(
                    [before] + [template] + ([after] if after else [])
                )
            )
        if not in_place(form, params[_TARGET], verse, clause.site.note, _KETIV_SIDE):
            raise AssertionError(f"{verse}: a written pointed ketiv is not in place")
        if trailing:
            self._tally(_TRAILING_MAQAF, verse)
        self._tally(_TARGETS_CHANGED, bang=clause.bang)
        return _WRITTEN_ADJUSTED if adjustment else _WRITTEN_AS_IT_STANDS

    def _check_pointed_ketiv(
        self, portion, carriers, ketiv, qere, adjustment, site, verse
    ):
        """Raise unless ``portion`` may be written as the pointed ketiv of a template
        whose parameters 1 and 2 are ``ketiv`` and ``qere``; return whether it ends in
        the qere's trailing maqaf.

        ``carriers`` is None, or at Isaiah 36:12 the carriers of the near-Aleppo dataset's rule-8 template,
        which ``portion`` follows after a space. The carriers and ``portion`` must hold
        letters, marks, spaces and maqafs alone, nothing of _NOT_IN_POINTED_KETIV, no
        ZERO WIDTH NON-JOINER but the one _ZERO_WIDTH_NON_JOINER_READINGS names, and
        neither configuration of _PHASE3_CONFIGURATION_READINGS. ``portion`` must have
        no doubled or outer space, and the ketiv's letters as written, final forms
        included, and its spaces and maqafs the ketiv's, except for a trailing maqaf,
        which must be the qere's, and at the site of _MAQAF_FOR_KETIV_SPACE, where the
        ketiv's one space is a maqaf.
        """
        whole = portion if carriers is None else carriers + " " + portion
        for char, name in _NOT_IN_POINTED_KETIV.items():
            if char in whole:
                raise AssertionError(f"{verse}: a pointed ketiv holding {name}")
        joiners = whole.count(_ZERO_WIDTH_NON_JOINER)
        if joiners:
            if _ZERO_WIDTH_NON_JOINER_READINGS.get(verse) != site or joiners != 1:
                raise AssertionError(
                    f"{verse}: a pointed ketiv holding {joiners} ZERO WIDTH "
                    "NON-JOINER, where _ZERO_WIDTH_NON_JOINER_READINGS names none"
                )
            self._uses["_ZERO_WIDTH_NON_JOINER_READINGS"] += 1
        allowed = phase3._LETTERS | phase3._MARKS | {" ", _ZERO_WIDTH_NON_JOINER}
        if any(char not in allowed for char in whole):
            raise AssertionError(
                f"{verse}: a pointed ketiv holding a character it cannot have"
            )
        if portion != portion.strip() or "  " in portion:
            raise AssertionError(
                f"{verse}: a pointed ketiv with an outer or a doubled space"
            )
        if _configurations(whole):
            raise AssertionError(
                f"{verse}: a pointed ketiv with {_configurations(whole)}, a "
                "configuration a phase 3 policy removes"
            )
        if phase3._spelling(portion) != phase3._spelling(ketiv):
            raise AssertionError(
                f"{verse}: a pointed ketiv whose letters are not the ketiv's"
            )
        skeleton = _skeleton(ketiv)
        if adjustment == _MAQAF_FOR_KETIV_SPACE:
            if skeleton.count(" ") != 1:
                raise AssertionError(
                    f"{verse}: a ketiv with other than one space, where the table "
                    "assumes one"
                )
            skeleton = skeleton.replace(" ", phase3.MAQAF)
        if qere.endswith(phase3.MAQAF) and not portion.endswith(phase3.MAQAF):
            raise AssertionError(
                f"{verse}: a pointed ketiv omitting the qere's trailing maqaf"
            )
        trailing = portion.endswith(phase3.MAQAF) and not ketiv.endswith(phase3.MAQAF)
        if trailing:
            if not qere.endswith(phase3.MAQAF):
                raise AssertionError(
                    f"{verse}: a pointed ketiv ending in a maqaf that the qere lacks"
                )
            skeleton += phase3.MAQAF
        if _skeleton(portion) != skeleton:
            raise AssertionError(
                f"{verse}: a pointed ketiv whose spaces and maqafs are not the ketiv's"
            )
        return trailing

    def _check_configurations(self, form, site, verse):
        """Raise unless an applied form has a configuration a phase 3 policy removes
        exactly where _PHASE3_CONFIGURATION_READINGS names it."""
        found = _configurations(form)
        if not found:
            return
        named = _PHASE3_CONFIGURATION_READINGS.get(verse)
        if named is None or named[0] != site or found != [named[1]]:
            raise AssertionError(
                f"{verse}: an applied reading has {found}, a configuration a phase 3 "
                "policy removes, where _PHASE3_CONFIGURATION_READINGS does not name it"
            )
        self._uses["_PHASE3_CONFIGURATION_READINGS"] += 1
        self._tally(_CONFIGURATIONS, verse)

    def _tally(self, label, verse=None, bang=False):
        """Count one of ``label``, at ``verse`` if its sites are kept, and once more
        under its bang-marked label if ``bang``."""
        self.counts[label] += 1
        if bang:
            self.counts[label + _BANG] += 1
        if verse is not None:
            self.sites[label].append(verse)


def notes(cell, verse):
    """The נוסח templates of an E cell, in the order the walk meets them.

    The walk follows phase 2's rule table along each kept template's selected
    parameters, as phase2.selected_keys names them, and stops at each נוסח, entering
    neither its target nor its body, as the census's each_nusach does. It meets the
    notes in the census's order, as many as the census counts, which
    build_expectations.assert_census_agrees checks; none is in the target of another. A template that phase 2 dissolves, or
    replaces by a placeholder, cannot be
    in an E cell that phase 3 returns, and raises. The near-Aleppo dataset's rule-8 template, which a pointed
    ketiv can hold, holds no note.
    """
    found = []
    _walk(cell, verse, found)
    return found


def _walk(value, verse, found):
    if isinstance(value, str):
        return
    if isinstance(value, list):
        for item in value:
            _walk(item, verse, found)
        return
    name = value["tmpl_name"]
    rule = phase2._RULES.get(name)
    if rule is None:
        raise AssertionError(
            f"{verse}: phase 5 met {name!r}, which phase 2 has no rule for"
        )
    if name == _NOTE:
        found.append(value)
    elif rule.action in (phase2._KEEP_NOTE, phase2._KEEP_KQ):
        for key in phase2.selected_keys(value, verse):
            _walk(value["tmpl_params"][key], verse, found)
    elif rule.action not in (phase2._VERBATIM, phase2._COLLAPSE_WORD, phase2._CARRIERS):
        raise AssertionError(
            f"{verse}: phase 5 met {name!r}, a template phase 2 does not keep"
        )


def reading_side(sigla, verse, site):
    """The side of its note's target that a clause's forms are compared with.

    ``sigla`` are the clause's codex sigla, as (siglum, qualifier) pairs, and ``site``
    its Site in ``verse``. A clause headed א-כתיב, or one that _KETIV_LETTERS_READINGS
    names, reads the ketiv side; one headed א-קרי, the qere side; and every other
    clause, the selected text. Codex sigla mixing a plane's siglum with another raise,
    no policy saying which side such a clause reads.
    """
    bases = {siglum for siglum, _ in sigla}
    plane = bases & _PLANE_SIGLA
    if plane and (len(plane) > 1 or bases - plane):
        raise AssertionError(
            f"{verse}: a clause whose codex sigla {sorted(bases)} mix a ketiv/qere "
            "plane's siglum with another"
        )
    if _KETIV_SIGLUM in plane or _KETIV_LETTERS_READINGS.get(verse) == site:
        return _KETIV_SIDE
    if _QERE_SIGLUM in plane:
        return _QERE_SIDE
    return _SELECTED_SIDE


def in_place(form, target, verse, note, side):
    """Whether a quoted ``form`` is in place in ``target``, on ``side``.

    ``target`` is the target of note ``note`` of ``verse``, the note's 1-based position
    among the נוסח that notes() finds, ``form`` a form a clause of that note quotes,
    as phase3._quoted_forms reads it, and ``side`` what reading_side gives for the
    clause. It is in place where, with HEBREW POINT QAMATS QATAN changed to HEBREW
    POINT QAMATS and any trailing "?" removed, it equals the target read on that side:
    each ketiv/qere template read by the parameters _SIDE_KEYS names for the side, or,
    for the selected text, by phase2.selected_keys. A form read on the ketiv side at a
    note of _POINTED_KETIV_ADJUSTMENTS whose adjustment is _WITHOUT_MASORA_CIRCLES is
    compared less its HEBREW MARK MASORA CIRCLE. On the selected text it is also in
    place, at a note of _FORM_WITHOUT_PASEQ_READINGS, where it equals that text less
    the one HEBREW PUNCTUATION PASEQ that ends it, and at a note of
    _SUB_SPAN_READINGS, where it equals the named atoms of that text. The near-Aleppo dataset's rule-8 template
    reads as MAM's notes write such marks, in square brackets. This is the one
    in-place test: phase 5 applies the readings not in place, and phase6_flags.py's
    rules call it too.
    """
    return _in_place_kind(form, target, verse, note, side) is not None


def _in_place_kind(form, target, verse, note, side):
    """How in_place finds ``form`` in place, or None where it is not."""
    form = _canonical(form).rstrip("?")
    named = _POINTED_KETIV_ADJUSTMENTS.get(verse)
    if (
        side == _KETIV_SIDE
        and named is not None
        and named[0].note == note
        and named[1] == _WITHOUT_MASORA_CIRCLES
    ):
        form = form.replace(_MASORA_CIRCLE, "")
    text = _side_text(target, verse, side)
    if form == text:
        return _AS_SELECTED if side == _SELECTED_SIDE else _ON_ITS_SIDE
    if side != _SELECTED_SIDE:
        return None
    paseq = _FORM_WITHOUT_PASEQ_READINGS.get(verse)
    if paseq is not None and paseq.note == note:
        if not text.endswith(phase3.PASEQ) or text.count(phase3.PASEQ) != 1:
            raise AssertionError(
                f"{verse}: a target _FORM_WITHOUT_PASEQ_READINGS names that does not "
                "end in its one paseq glyph"
            )
        if form == text[:-1]:
            return _WITHOUT_PASEQ
    sub_span = _SUB_SPAN_READINGS.get(verse)
    if sub_span is not None and sub_span[0].note == note:
        start, end = _named_span(text, sub_span, verse)
        if form == text[start:end]:
            return _NAMED_ATOMS
    return None


def _named_span(text, sub_span, verse):
    """The start and end in ``text`` of the atoms a _SUB_SPAN_READINGS entry names."""
    _, first, last, count = sub_span
    atoms = phase3._atoms(text)
    if len(atoms) != count:
        raise AssertionError(
            f"{verse}: a target _SUB_SPAN_READINGS names has {len(atoms)} atoms, not "
            f"{count}"
        )
    last_index, last_marks = atoms[last - 1][-1]
    return atoms[first - 1][0][0], max([last_index] + last_marks) + 1


def _side_text(target, verse, side):
    """The text of ``target`` read on ``side``, as in_place reads it."""
    if side == _SELECTED_SIDE:
        return phase3._selected_text(target, verse)
    return phase3._selected_text(
        target, verse, lambda tmpl, verse: _side_keys(tmpl, verse, side)
    )


def _side_keys(tmpl, verse, side):
    """The keys of ``tmpl``'s parameters read on ``side``, the ketiv side or the qere
    side, a kept note or ketiv/qere template.

    A note template reads its selected parameter, and a ketiv/qere template the
    parameters _SIDE_KEYS names, except that the ketiv side of an ordinary family with
    a pointed ketiv is its pointed ketiv, its selected parameter. A ketiv/qere family
    _SIDE_KEYS does not name, or a side it does not give a family, raises.
    """
    selected = phase2.selected_keys(tmpl, verse)
    name = tmpl["tmpl_name"]
    if phase2._RULES[name].action != phase2._KEEP_KQ:
        return selected
    if name not in _SIDE_KEYS or side not in _SIDE_KEYS[name]:
        raise AssertionError(f"{verse}: no {side} of a {name}, which in_place reads")
    if side == _KETIV_SIDE and selected == (phase2.POINTED_KETIV_PARAMETER,):
        return selected
    return _SIDE_KEYS[name][side]


def _direct_ketiv_qere_target(value, verse, site):
    """Validate a ketiv/qere-plane target's direct structure.

    Return its one recognized direct ketiv/qere template, its position, and the plain
    text before and after it. Return None only at the exact plane sites named by
    _PHASE3_REPLACED_PLANE_READINGS, where phase 3 replaced the template. No parameter
    is searched recursively.
    """
    elements = phase2._as_list(value)
    found = []
    for index, element in enumerate(elements):
        if isinstance(element, str):
            continue
        if not isinstance(element, dict):
            raise AssertionError(
                f"{verse}: a ketiv/qere-plane target has a direct element that is "
                f"neither plain text nor a template: {element!r}"
            )
        name = element.get("tmpl_name")
        if not isinstance(name, str):
            raise AssertionError(
                f"{verse}: a ketiv/qere-plane target has a malformed direct "
                f"template: {element!r}"
            )
        if name not in _KETIV_QERE_SCRIPTURE_KEYS:
            kind = "unrelated recognized" if name in phase2._RULES else "unknown"
            raise AssertionError(
                f"{verse}: a ketiv/qere-plane target has {kind} direct template "
                f"{name!r}; intervening wrappers and recursive discovery are not "
                "allowed"
            )
        if set(element) != {"tmpl_name", "tmpl_params"}:
            raise AssertionError(
                f"{verse}: direct {name!r} in a ketiv/qere-plane target has "
                f"unexpected object keys {sorted(element)!r}"
            )
        params = element["tmpl_params"]
        if not isinstance(params, dict):
            raise AssertionError(
                f"{verse}: direct {name!r} in a ketiv/qere-plane target has "
                f"non-mapping parameters {params!r}"
            )
        base_keysets = phase2._RULES[name].keysets
        allowed_keysets = base_keysets
        if name in phase2.POINTED_KETIV_FAMILIES:
            allowed_keysets = allowed_keysets | frozenset(
                keys | {phase2.POINTED_KETIV_PARAMETER} for keys in base_keysets
            )
        if frozenset(params) not in allowed_keysets:
            raise AssertionError(
                f"{verse}: direct {name!r} in a ketiv/qere-plane target has "
                f"unexpected parameters {sorted(params)!r}"
            )
        scripture_keys = _KETIV_QERE_SCRIPTURE_KEYS[name]
        for key, child in params.items():
            if key == phase2.POINTED_KETIV_PARAMETER:
                if isinstance(child, str):
                    continue
                if (
                    not isinstance(child, list)
                    or len(child) != 2
                    or not isinstance(child[0], dict)
                    or set(child[0]) != {"tmpl_name", "tmpl_params"}
                    or child[0].get("tmpl_name") != phase2.MARKS_WITHOUT_LETTER
                    or not isinstance(child[1], str)
                    or not child[1].startswith(" ")
                    or child[1].startswith("  ")
                ):
                    raise AssertionError(
                        f"{verse}: direct {name!r} pointed-ketiv parameter has "
                        "neither plain text nor the near-Aleppo dataset's rule-8 exact structure"
                    )
                try:
                    phase2.carriers_text(child[0], verse)
                except (AssertionError, KeyError, TypeError) as error:
                    raise AssertionError(
                        f"{verse}: direct {name!r} pointed-ketiv parameter has a "
                        "malformed rule-8 template specific to the near-Aleppo dataset"
                    ) from error
                continue
            if not isinstance(child, str):
                role = (
                    "Scripture-bearing parameter"
                    if key in scripture_keys
                    else "apparatus parameter"
                )
                raise AssertionError(
                    f"{verse}: direct {name!r} {role} {key!r} is not plain text; "
                    "nested templates are not allowed"
                )
        found.append((index, element))
    if len(found) > 1:
        raise AssertionError(
            f"{verse}: a ketiv/qere-plane target has {len(found)} direct "
            "ketiv/qere templates, not 1"
        )
    replacement_site = _PHASE3_REPLACED_PLANE_READINGS.get(verse)
    if not found:
        if replacement_site != site:
            raise AssertionError(
                f"{verse}: a ketiv/qere-plane target has no direct ketiv/qere "
                "template and is not an explicitly named phase-3 replacement"
            )
        if not isinstance(value, str):
            raise AssertionError(
                f"{verse}: an explicitly named phase-3 replacement whose target is "
                "not plain text"
            )
        if not any(
            disposition != phase3._KQ_KEPT
            for disposition, _, _ in phase3._KQ_SITES.get(verse, ())
        ):
            raise AssertionError(
                f"{verse}: _PHASE3_REPLACED_PLANE_READINGS names {site}, but phase "
                "3 has no replacing ketiv/qere-apparatus site there"
            )
        return None
    if replacement_site == site:
        raise AssertionError(
            f"{verse}: _PHASE3_REPLACED_PLANE_READINGS names {site}, but the direct "
            "ketiv/qere template remains"
        )
    ((index, template),) = found
    return _DirectKetivQereTarget(
        template, index, "".join(elements[:index]), "".join(elements[index + 1 :])
    )


def _portion(form, before, after, verse):
    """``form`` less ``before`` and ``after``, the target's text before and after its
    ketiv/qere template, cut as phase3._note_form_less_target cuts a form."""
    if (
        len(form) < len(before) + len(after)
        or not form.startswith(before)
        or not form.endswith(after)
    ):
        raise AssertionError(
            f"{verse}: the note's form lacks the target's text around the ketiv/qere "
            "template"
        )
    return form[len(before) : len(form) - len(after)]


def _skeleton(text):
    """The letters, spaces and maqafs of ``text``, in order, all else left out."""
    return "".join(
        char for char in text if char in phase3._LETTERS or char in (" ", phase3.MAQAF)
    )


def _check_pending_plane(clause, target, direct_target, why, side, verse):
    """Raise unless a reading _PENDING_PLANE_READINGS names has the shape ``why``
    describes, and is not in place on ``side``, the ketiv side, at the validated
    direct ketiv/qere template."""
    if direct_target is None or side != _KETIV_SIDE or len(clause.forms) != 1:
        raise AssertionError(
            f"{verse}: a pending plane reading that is not one form headed א-כתיב at "
            "one direct ketiv/qere template"
        )
    (form,) = clause.forms
    params = direct_target.template["tmpl_params"]
    ketiv = params["1"]
    if not isinstance(ketiv, str):
        raise AssertionError(f"{verse}: a consonantal ketiv that is not plain text")
    if why == _TWO_RENDERINGS:
        shaped = len(_GUILLEMET_RUN.findall(form)) == 2 and "+" in form
    elif why == _SECOND_WORD_ALONE:
        words = ketiv.split(" ")
        shaped = len(words) == 2 and phase3._spelling(form) == words[1]
    elif why == _NO_SEPARATOR_AFTER:
        qere = params["2"]
        shaped = (
            isinstance(qere, str)
            and qere.endswith(phase3.MAQAF)
            and phase3._spelling(form) == phase3._spelling(ketiv)
            and form[-1] not in (" ", phase3.MAQAF)
        )
    else:
        raise AssertionError(f"{verse}: no pending plane reading of shape {why!r}")
    if not shaped:
        raise AssertionError(
            f"{verse}: a pending plane reading without the shape its table names: {why}"
        )
    if in_place(form, target, verse, clause.site.note, side):
        raise AssertionError(f"{verse}: a pending plane reading in place already")


def _check_one_sided_plane(clause, target, direct_target, family, side, verse):
    """Raise unless a reading _ONE_SIDED_PLANE_READINGS names is headed א-כתיב at a
    target holding the validated direct ketiv/qere template of ``family``, and is not
    in place."""
    if (
        direct_target is None
        or side != _KETIV_SIDE
        or direct_target.template["tmpl_name"] != family
        or any(in_place(f, target, verse, clause.site.note, side) for f in clause.forms)
    ):
        raise AssertionError(
            f"{verse}: a plane reading _ONE_SIDED_PLANE_READINGS names that is not one "
            f"headed א-כתיב, not in place, at one {family}"
        )


def _classified(site, sigla, rest, verse):
    """(disposition, reason, _Clause) of a direct differing clause."""
    disposition, reason, forms = _disposition(sigla, rest)
    bang = any("!" in qualifier and "?" not in qualifier for _, qualifier in sigla)
    if disposition == _APPLY and forms[0] != forms[0].strip():
        raise AssertionError(f"{verse}: an apply-candidate's form has an outer space")
    return disposition, reason, _Clause(site, sigla, rest, tuple(forms), bang)


def _disposition(sigla, rest):
    """The oracle's (disposition, reason, forms) for a clause with ``sigla``, each a
    (siglum, qualifier), and ``rest``, its text after its "=". The tests run in the
    oracle's order."""
    forms = [_canonical(form) for form in phase3._quoted_forms(rest)]
    if any("?" in qualifier for _, qualifier in sigla):
        return _DO_NOT_APPLY, _DOUBT_SIGLUM, forms
    if not any(char in _POINTED for char in _reading_head(rest)):
        return _DO_NOT_APPLY, _PROSE_DESCRIPTION, forms
    if forms and forms[0].rstrip().endswith("?"):
        return _DO_NOT_APPLY, _DOUBT_FORM, forms
    if any(siglum in _PLANE_SIGLA for siglum, _ in sigla):
        return _PENDING, _KETIV_QERE_PLANE, forms
    if len(forms) != 1:
        return _PENDING, f"candidate-form-count-{len(forms)}", forms
    if any(char in forms[0] for char in _PUNCTUATION):
        return _PENDING, _FORM_PUNCTUATION, forms
    return _APPLY, _SINGLE_POINTED_FORM, forms


def _reason_label(disposition, reason):
    """The label a clause with this disposition and reason is counted under."""
    return f"codex readings: {disposition} ({reason})"


def _reading_head(rest):
    """The form a clause offers, as the oracle reads it for pointedness: its
    angle-bracketed runs, joined by spaces, where there are any, and otherwise its
    text before its first " ("."""
    runs = phase3._ANGLE_RUN.findall(rest)
    if runs:
        return " ".join(runs)
    cut = rest.find(" (")
    return rest[:cut] if cut >= 0 else rest


def _canonical(form):
    """``form`` with phase 3's qamats-size policy applied."""
    return form.replace(phase3.QAMATS_QATAN, phase3.QAMATS)


def _check_replacement(form, replaced, verse):
    """Raise unless ``form`` can stand in the dataset in place of ``replaced``.

    It must hold letters, marks and single spaces alone, and no varika or masora
    circle; and it must have the spaces and maqafs of the text it replaces, and as
    many paseq glyphs and SOF PASUQ characters, so that a reading never drops a
    legarmeh or a paseq, nor changes a maqaf, which phase 3's maqaf policy decides.
    """
    allowed = (
        phase3._LETTERS
        | (phase3._MARKS - {phase3.VARIKA, "\N{HEBREW MARK MASORA CIRCLE}"})
        | {" "}
    )
    if any(char not in allowed for char in form):
        raise AssertionError(f"{verse}: a reading holding a character it cannot have")
    if form != form.strip() or "  " in form:
        raise AssertionError(f"{verse}: a reading with an outer or a doubled space")
    if _separators(form) != _separators(replaced):
        raise AssertionError(
            f"{verse}: a reading whose spaces and maqafs are not those of the text it "
            "replaces"
        )
    if form.count(phase3.PASEQ) != replaced.count(phase3.PASEQ):
        raise AssertionError(
            f"{verse}: a reading with a paseq glyph more or less than the text it "
            "replaces"
        )

    if form.count("\N{HEBREW PUNCTUATION SOF PASUQ}") != replaced.count(
        "\N{HEBREW PUNCTUATION SOF PASUQ}"
    ):
        raise AssertionError(
            f"{verse}: a reading with a SOF PASUQ more or less than the text it replaces"
        )


def _separators(text):
    return [char for char in text if char in (" ", phase3.MAQAF)]


def _configurations(form):
    """The configurations in ``form`` that a phase 3 policy removes from MAM's text,
    of the two _PHASE3_CONFIGURATION_READINGS names."""
    found = []
    for atom in phase3._atoms(form):
        for _, marks in atom:
            chars = [form[index] for index in marks]
            if phase3.OLE in chars and phase3.YORED in chars:
                found.append(_OLE_AND_YORED)
        letters = "".join(form[index] for index, _ in atom[-4:])
        if len(atom) >= 4 and letters == phase3._DIVINE_NAME_LETTERS:
            (_, _), (_, he), (_, vav), _ = atom[-4:]
            vav_marks = [form[index] for index in vav]
            if (
                phase3.QAMATS in vav_marks
                and phase3.HIRIQ not in vav_marks
                and phase3.HOLAM in [form[index] for index in he]
            ):
                found.append(_ADONAI_READING_HOLAM)
    return found


def _check_ketiv_letters(form, target, verse):
    """Raise unless ``form`` has the letters of ``target`` read on the ketiv side of
    its one כו״ק or קו״כ, and not those of its qere side."""
    elements = phase2._as_list(target)
    templates = [element for element in elements if isinstance(element, dict)]
    if len(templates) != 1 or templates[0]["tmpl_name"] not in _KETIV_LETTERS_FAMILIES:
        raise AssertionError(
            f"{verse}: a target _KETIV_LETTERS_READINGS names that does not hold one "
            "כו״ק or קו״כ"
        )
    ketiv = templates[0]["tmpl_params"]["1"]
    if not isinstance(ketiv, str):
        raise AssertionError(f"{verse}: a consonantal ketiv that is not plain text")
    ketiv_side = "".join(
        ketiv if isinstance(element, dict) else element for element in elements
    )
    letters = phase3._spelling(form)
    if letters != phase3._spelling(ketiv_side) or letters == phase3._spelling(
        phase3._selected_text(target, verse)
    ):
        raise AssertionError(
            f"{verse}: a reading _KETIV_LETTERS_READINGS names without the ketiv's "
            "letters"
        )


def _check_qere_without_ketiv(clause, target, verse):
    """Raise unless ``target`` holds a קרי ולא כתיב and the clause's form stops at a
    "[]"."""
    names = [
        element["tmpl_name"]
        for element in phase2._as_list(target)
        if isinstance(element, dict)
    ]
    if names != [_QERE_WITHOUT_KETIV]:
        raise AssertionError(
            f"{verse}: a target _QERE_WITHOUT_KETIV_READINGS names that does not hold "
            f"one {_QERE_WITHOUT_KETIV}"
        )
    tokens = clause.rest.strip().split(" ")
    taken = len(clause.forms[0].split(" "))
    if tokens[taken : taken + 1] != ["[]"]:
        raise AssertionError(
            f"{verse}: a form _QERE_WITHOUT_KETIV_READINGS names that does not stop at "
            'a "[]"'
        )


def _check_not_applied(clause, note, verse):
    """Raise unless the note still says what NOT_APPLIED_READINGS assumes: the reading
    is the testimony _SILENT_TESTIMONY's alone, it is not in place, and one agreeing
    clause cites _EXPLICIT_TESTIMONY."""
    params = note["tmpl_params"]
    if clause.sigla != ((_SILENT_TESTIMONY, ""),):
        raise AssertionError(
            f"{verse}: the reading NOT_APPLIED_READINGS names is not "
            f"{_SILENT_TESTIMONY}'s alone"
        )
    if in_place(
        clause.forms[0], params[_TARGET], verse, clause.site.note, _SELECTED_SIDE
    ):
        raise AssertionError(
            f"{verse}: the reading NOT_APPLIED_READINGS names is in place already"
        )
    agreeing = [
        text
        for text in phase3._clauses(params[_BODY], verse)
        if text.startswith("=") and _EXPLICIT_TESTIMONY in phase3._clause_sigla(text)
    ]
    if len(agreeing) != 1:
        raise AssertionError(
            f"{verse}: {len(agreeing)} agreeing clauses cite {_EXPLICIT_TESTIMONY}, "
            "not 1"
        )
