"""Document editorial choices and their alternatives.

The table records the adopted text or representation and alternatives not taken.
Names between backticks are isolated as Hebrew or rendered as code. Decision
dates order the source records; dates and authors are omitted from the table.
"""

import re
from typing import NamedTuple

from near_aleppo.doc_html import code
from near_aleppo.doc_html import he_name
from near_aleppo.doc_html import isolated
from near_aleppo.doc_html import link
from near_aleppo.doc_html import table
from mb_misc import mb_html

SECTION = ("choices", "Choices that could have gone another way")

_BEN = "Ben Denckla"
_EDITORIAL = "Editorial implementation"
_EDITORIAL_BEN_ACCEPTED = "Editorial implementation"
_EDITORIAL_BEN_CONFIRMED = "Editorial implementation"

_HEBREW_LETTER = re.compile("[\N{HEBREW LETTER ALEF}-\N{HEBREW LETTER TAV}]")


class Choice(NamedTuple):
    """One choice: its date, who made it, what it was about, what was chosen, and the
    alternatives not taken, the last two in the prose convention above."""

    date: str
    who: str
    topic: str
    chosen: str
    alternatives: tuple


# The choices, oldest first.
_CHOICES = (
    Choice(
        "2026-08-23",
        _BEN,
        "Leningrad as a proxy where the codex is lost",
        "Where the codex is lost and no testimony to it survives, near-Aleppo takes Leningrad, as MAM's apparatus records it, as an acceptable proxy for the codex.",
        (),
    ),
    Choice(
        "2026-08-23",
        _BEN,
        "The rafe marks MAM lacks",
        "Near-Aleppo has the rafe marks MAM has and no others, so it has fewer than the codex, which has the rafe in many places where MAM does not.",
        ("Deriving the missing rafe marks by rule",),
    ),
    Choice(
        "2026-08-25",
        _BEN,
        "The missing pointing of the divine name",
        "Where MAM does not supply the codex's pointing of the divine name, near-Aleppo documents that gap as a limitation.",
        ("Filling the divine-name pointing gap from another edition's text",),
    ),
    Choice(
        "2026-08-25",
        _BEN,
        "The doubled cantillation of `מ:כפול`",
        "Near-Aleppo has the parameter `כפול` of `מ:כפול`, which has the accents of both strands together, and not its single-strand parameters `א` and `ב`; this concerns the two Decalogues and Genesis 35:22.",
        (
            "The single-strand cantillation of parameter `א`",
            "The single-strand cantillation of parameter `ב`",
        ),
    ),
    Choice(
        "2026-08-25",
        _BEN,
        "A maqaf ending the qere",
        "Where near-Aleppo has a pointed ketiv made from the qere's pointing, a maqaf ending the qere counts as part of the pointing, so the pointed ketiv ends in it too.",
        ("Carrying the qere's vowels and accents onto the ketiv but not its maqaf",),
    ),
    Choice(
        "2026-08-25",
        _BEN,
        "The two parameters of `מ:קמץ`",
        "Near-Aleppo has the parameter `ד` of `מ:קמץ`, and not `ס`; once the qamats size and the gray-maqaf rule apply, the two give the same text at every one of MAM's `מ:קמץ`.",
        ("Parameter `ס`",),
    ),
    Choice(
        "2026-08-25",
        _BEN,
        "The gray maqaf",
        "Where MAM has a gray maqaf (`מ:מקף אפור`), near-Aleppo has a space between the two words, so they are chanted separately.",
        ("A maqaf, joining the two words into one chanted word",),
    ),
    Choice(
        "2026-08-25",
        _BEN,
        "The gray maqaf at Psalms 18:20 and 22:9",
        "At Psalms 18:20 and 22:9, where the codex is lost and MAM's introduction records other manuscripts with a written maqaf after one of the words that has a gray maqaf, near-Aleppo has a space at each gray maqaf of the two verses, as elsewhere.",
        ("Excepting the two verses and having a maqaf there",),
    ),
    Choice(
        "2026-08-25",
        _BEN,
        "How near-Aleppo has a legarmeh or a narrow-sense paseq",
        "Where MAM has `מ:לגרמיה-2` or `מ:פסק`, near-Aleppo has the one character Unicode PASEQ directly after the preceding word, with a space after it and none before, so near-Aleppo does not tell legarmeh from narrow-sense paseq.",
        (),
    ),
    Choice(
        "2026-08-25",
        _BEN,
        "What an agreeing clause citing the codex asserts",
        "A note clause opening with `=` whose sigla include the codex is read as agreeing with MAM on the point the note is about, not on every mark, so it does not stop a policy from removing a mark that MAM adds by convention.",
        ("Reading such a clause as saying the codex agrees with MAM in every mark",),
    ),
    Choice(
        "2026-08-25",
        _EDITORIAL_BEN_ACCEPTED,
        "The divine-name holam at 1 Kings 8:11, whose note names no source",
        "The note at 1 Kings 8:11 says a holam was written in the divine name but names no source, so near-Aleppo does not count it among the notes recording the codex's holam, and has no holam there.",
        (
            "Reading the missing siglum as `א`, the likely intent, and keeping the holam",
        ),
    ),
    Choice(
        "2026-08-25",
        _EDITORIAL_BEN_ACCEPTED,
        "The revia mugrash at Job 19:16",
        "At Job 19:16 near-Aleppo has the geresh muqdam on the first word of the maqaf compound and the revia on the second, as the note gives the codex's form, where MAM has both marks on one letter of the second word.",
        ("Removing the revia, as at the other sites",),
    ),
    Choice(
        "2026-08-25",
        _EDITORIAL_BEN_ACCEPTED,
        "The revia mugrash at Proverbs 19:26",
        "At Proverbs 19:26, where MAM's introduction records the codex as having the revia, though doubtfully, near-Aleppo has the revia as MAM has it, and the note has a `flagged-not-applied` flag.",
        (),
    ),
    Choice(
        "2026-08-26",
        _BEN,
        "The large he at Deuteronomy 32:6",
        "Near-Aleppo has MAM's `מ:אות-ג` at Deuteronomy 32:6, the one site where MAM says the codex has the special letter, and plain letters at the other special-letter sites, the suspended letters apart.",
        (
            "Plain letters there as at the others, as it stood until MAM's statements about the verse were corrected that day",
        ),
    ),
    Choice(
        "2026-08-31",
        _BEN,
        "Forms that MAM's notes mark as manifest errors in the codex",
        "Where a note's clause cites the codex with a bang (`!`), marking a manifest error in the codex, near-Aleppo has the clause's form, the scribe's slip included, flagged `applied-and-flagged` so that it can be reversed.",
        ("Not applying those forms, which would make near-Aleppo a corrected codex",),
    ),
    Choice(
        "2026-09-01",
        _BEN,
        "The zarqa stress helpers no note records",
        "Near-Aleppo has no zarqa stress helper where no note keeps one, on the assumption that the codex likely has none there; the sites were not inspected, and where the codex is lost no manuscript was read.",
        ("Inspecting the sites",),
    ),
    Choice(
        "2026-09-01",
        _BEN,
        "Stress helpers that a note records",
        "Near-Aleppo has MAM's stress helper wherever a note records the codex doubling the accent and, where the codex is lost, wherever a note records a respected manuscript doing so, Leningrad counting as respected.",
        (
            "No stress helper at those words either, by position, as the stress-helper rules alone would have it",
            "At a lost verse, not counting a note that cites only Leningrad as reason to keep the stress helper",
        ),
    ),
    Choice(
        "2026-09-01",
        _BEN,
        "Marks the codex has where no letter is written",
        "The original decision puts vowels and accents that the codex has with no letter under them on artificial alef carriers in a template specific to near-Aleppo, `ניקוד בלי אות`, first used at Isaiah 36:12.",
        (
            "An empty body text at every `קרי ולא כתיב`, with 2 Samuel 18:20's marks documented as marks near-Aleppo cannot hold",
        ),
    ),
    Choice(
        "2026-09-01",
        _BEN,
        "The carrier letter of the templates for marks without a letter",
        "The original GA convention puts the marks on alefs, an arbitrary carrier, rather than on a letter matching the unwritten word. The later GV extension is recorded separately below.",
        ("A placeholder matching the unwritten word, such as a bet at 2 Samuel 18:20",),
    ),
    Choice(
        "2026-09-01",
        _BEN,
        "The prefix of near-Aleppo's template names",
        "The two template names have no `מ:` prefix, which marks MAM's templates, and every mention of them says that they are specific to the near-Aleppo dataset.",
        ("The `מ:` prefix that MAM's templates have",),
    ),
    Choice(
        "2026-09-01",
        _BEN,
        "Marks at a position of no width",
        "The decision reserves the name `ניקוד בלי אות ובלי רווח` for a planned template specific to near-Aleppo, intended to represent marks at a position of no width, at the join inside a maqaf compound. Its intended use at 2 Samuel 18:20 remains pending.",
        ("A parameter of the one template",),
    ),
    Choice(
        "2026-09-01",
        _BEN,
        "How the edition has marks written where no letter is",
        "The edition has the marks of the templates for marks without a letter, specific to the near-Aleppo dataset, in double guillemets.",
        (
            "Square brackets",
            "Single guillemets",
        ),
    ),
    Choice(
        "2026-09-01",
        _BEN,
        "A dagesh on a carrier alef",
        "A dagesh is outside the templates for marks without a letter, specific to the near-Aleppo dataset, and the build refuses one on a carrier alef; Ben read the codex at 2 Samuel 18:20 and found no dagesh among the marks there.",
        (),
    ),
    Choice(
        "2026-09-01",
        _BEN,
        "The maqaf after the unread ketiv at 2 Samuel 13:33",
        "At 2 Samuel 13:33, whose ketiv without a qere has no note, near-Aleppo has MAM's maqaf after the unread ketiv, flagged `flagged-not-applied`.",
        (
            "No maqaf there, by analogy with 2 Kings 5:18, whose note gives the codex's form without it",
        ),
    ),
    Choice(
        "2026-09-01",
        _BEN,
        "A ketiv/qere where MAM's note says the codex has no qere note",
        "Where MAM's note says the codex has no qere note, near-Aleppo has no ketiv/qere template, the codex's form standing as plain text in the note's target; Jeremiah 33:26 keeps its template, the note's form being doubt-marked.",
        ("Keeping MAM's ketiv/qere encoding at those verses",),
    ),
    Choice(
        "2026-09-01",
        _BEN,
        "The doubled geresh at Ezekiel 48:10",
        "At Ezekiel 48:10 near-Aleppo has the form the note gives the codex, with the geresh and the telisha gedolah both on the vav and neither on the alef.",
        ("MAM's form, flagged",),
    ),
    Choice(
        "2026-09-01",
        _BEN,
        "Masorah near-Aleppo leaves out",
        "Near-Aleppo has no masorah circles and no marginal masorah; the ketiv/qere apparatus is the one part of the masorah it has.",
        (),
    ),
    Choice(
        "2026-09-01",
        _BEN,
        "What the edition looks like",
        "The edition is to be rendered, in most ways, just as MAM-with-doc is rendered.",
        (),
    ),
    Choice(
        "2026-09-02",
        _BEN,
        "Where the marks go when a ketiv is pointed from its qere",
        "Each vowel and accent goes onto the ketiv's copy of the letter it sits on in the qere, not onto the letter in the same position, which chapter 2 of MAM's introduction names as the codex's convention.",
        (
            "By position, the marks in the order they come in the qere, which chapter 2 names as Leningrad's and the printed editions' way",
            "The two principles combined, a third way Yeivin describes",
        ),
    ),
    Choice(
        "2026-09-02",
        _BEN,
        "The codex's method, `שיטת-א`, where the codex is lost",
        "A `שיטת-א` clause counts as the codex where the codex is lost and not where it survives: at a lost verse near-Aleppo keeps MAM's text where such a clause agrees with MAM, and has the clause's form where it differs, except at Leviticus 10:4, where the note's `א(ס)` testimony prevails.",
        (
            "Excluding `שיטת-א` everywhere, as the rules did until then",
            "At a lost verse, Leningrad's form in place of MAM's, as the proxy rule would have it",
        ),
    ),
    Choice(
        "2026-09-02",
        _BEN,
        "Sites of `מ:קו״כ-אם-2` where MAM's apparatus is silent about the codex",
        "Near-Aleppo keeps MAM's `מ:קו״כ-אם-2` encoding, and where MAM's apparatus is silent about whether the codex has a qere note, the site is flagged `flagged-not-applied`, silence not being denial.",
        (),
    ),
    Choice(
        "2026-09-02",
        _BEN,
        "The ketiv/qere at Deuteronomy 29:22",
        "At Deuteronomy 29:22, whose note implies, by setting the word beside Psalms 79:10, that the codex has no qere note there without saying so, near-Aleppo keeps the ketiv/qere template and the note is flagged `flagged-not-applied`.",
        (),
    ),
    Choice(
        "2026-09-02",
        _BEN,
        "A manual check of the flagged `מ:קו״כ-אם-2` sites",
        "The flagged `מ:קו״כ-אם-2` sites stay flagged in a first version: settling them by eye against images of the codex and the Jerusalem Crown is tractable, but was not done.",
        ("Settling them by eye now",),
    ),
    Choice(
        "2026-09-02",
        _BEN,
        "The representation policies where the codex is lost",
        "Every representation policy applies at every verse, where the codex is lost as well as where it survives; what shrinks at a lost verse is only the supply of the codex's forms from MAM's notes.",
        (
            "MAM's text unchanged at a verse where the codex is lost, as a draft proposed",
        ),
    ),
    Choice(
        "2026-09-13",
        _BEN,
        "Templates in the other parameters of a ketiv/qere template",
        "Templates within a kept ketiv/qere template follow the same rules for evaluation or retention in every parameter, whether near-Aleppo's text follows it or not, so that templates such as `מ:קמץ` occur nowhere in near-Aleppo's text outside the copies of MAM's target.",
        (
            "Evaluating away templates only in the parameter near-Aleppo's text follows, retaining the other parameters verbatim, as in the first build",
        ),
    ),
    Choice(
        "2026-09-13",
        _BEN,
        "The conventions in the other parameters of a ketiv/qere template",
        "Near-Aleppo's conventions apply in every parameter of a kept ketiv/qere template, whether near-Aleppo's text follows it or not, so that Genesis 13:3's pointed qere, parameter `3` of its `מ:קו״כ-אם-2`, has a HEBREW POINT QAMATS where MAM has a HEBREW POINT QAMATS QATAN.",
        (
            "The conventions applied only in the parameter near-Aleppo's text follows, the others merely counted",
        ),
    ),
    Choice(
        "2026-09-13",
        _BEN,
        "Deferring the inferred pointed ketiv",
        "Inference was deferred at this stage. The approved frozen subset of 2026-10-02 supersedes this deferral for its accepted sites; remaining sites keep MAM's consonantal ketiv and pointed qere unless MAM's notes supply a pointed ketiv.",
        (),
    ),
    Choice(
        "2026-09-14",
        _BEN,
        "The space at the end of a note's target",
        "Where `מ:פסק` or `מ:מקף אפור` ends a note's target in MAM, near-Aleppo has the space that template supplies inside the target, so such a target ends in a space.",
        ("The space after the note template instead",),
    ),
    Choice(
        "2026-09-14",
        _BEN,
        "The revia mugrash in the lost stretch of Psalms",
        "At the sites in Psalms 15:1–25:1, where the codex is lost and chapter 5 of MAM's introduction records Leningrad as having the revia beside the geresh muqdam, near-Aleppo has the geresh muqdam without the revia, the form each note's `שיטת-א` clause gives.",
        (
            "The revia, on Leningrad's evidence as MAM records it, as planned until then",
        ),
    ),
    Choice(
        "2026-09-14",
        _BEN,
        "The revia at Psalms 105:2, where MAM's note and chapter 5 disagree",
        "The codex was read before deciding; Ben read it on 2026-09-15 as having the revia, as chapter 5 of MAM's introduction says, and near-Aleppo has the revia.",
        (),
    ),
    Choice(
        "2026-09-15",
        _BEN,
        "Isaiah 26:20, where the note says the codex has MAM's ketiv and no qere note",
        "Near-Aleppo has MAM's ketiv there pointed by the letter-driven transplant of the qere's pointing, the note giving no pointed form.",
        (
            "MAM's template kept until near-Aleppo infers pointed ketivs",
            "The ketiv unpointed",
            "Reading the codex first",
        ),
    ),
    Choice(
        "2026-09-15",
        _BEN,
        "A note whose target near-Aleppo changes",
        "Every note whose target near-Aleppo changes also has MAM's target, so that each of the note's clauses keeps MAM's text as its subject.",
        (),
    ),
    Choice(
        "2026-09-15",
        _BEN,
        "Where the copy of MAM's target is held",
        "The copy of MAM's target is a parameter added to the note.",
        ("A file beside the book files",),
    ),
    Choice(
        "2026-09-15",
        _BEN,
        "Which note templates have MAM's target",
        "The scroll-difference note, `מ:הערה-2`, has the copy of MAM's target, as `נוסח` does.",
        ("The note `נוסח` alone",),
    ),
    Choice(
        "2026-09-15",
        _EDITORIAL,
        "What counts as a changed note target",
        "A note's target counts as changed wherever near-Aleppo's parameter `1` differs from MAM-parsed-plus's, with no judgment about whether the change touches the note's point.",
        ("Judging, note by note, whether a change touches the note's point",),
    ),
    Choice(
        "2026-09-15",
        _BEN,
        "The name of the parameter holding MAM's target",
        "The parameter is named `מקרא על פי המסורה`, MAM's Hebrew name.",
        (
            "The name `mam`",
            "The name `יעד מקורי`",
        ),
    ),
    Choice(
        "2026-09-16",
        _BEN,
        "The codex's hataf hiriq",
        "At the letters where chapter 2 of MAM's introduction says the codex has a hataf hiriq, near-Aleppo has a sheva and a hiriq, the form each note gives the codex.",
        (
            "A hiriq alone",
            "MAM's varika kept",
        ),
    ),
    Choice(
        "2026-09-16",
        _EDITORIAL,
        "The hataf at Jeremiah 31:32, where two clauses disagree",
        "Near-Aleppo has the hataf patah of the clause headed `ל`, the one clause that cites a manuscript for a hataf.",
        (
            "The hataf qamats of the clause naming Ben-Asher, most printed editions, and Koren, which cites no manuscript",
        ),
    ),
    Choice(
        "2026-09-16",
        _BEN,
        "Whether a mater lectionis counts as a letter between the pashta's two copies",
        "A mater counts as a letter between, so near-Aleppo has the pashta's stress helper wherever MAM has it except where it is on the word's second-to-last letter.",
        (
            "A mater not counting",
            "Deferring the pashta",
        ),
    ),
    Choice(
        "2026-09-16",
        _BEN,
        "The pashta's stress helper where the codex is lost",
        "The pashta's convention applies where the codex is lost too.",
        ("Keeping the pashta's stress helper where the codex is lost",),
    ),
    Choice(
        "2026-09-16",
        _BEN,
        "The telisha gedolah word at Leviticus 10:4",
        "Near-Aleppo follows the note's `א(ס)` testimony there, with the telisha gedolah on the qof and the gershayim on the bet, the form of the note's clause headed `ל,ל1,ב,ש,ו?`.",
        (
            "The stress-helper rule for the word as first written",
            "MAM's form kept",
        ),
    ),
    Choice(
        "2026-09-16",
        _BEN,
        "How near-Aleppo has a flag",
        "A flag is a parameter added to the template it concerns: the `נוסח` whose clause motivates it or, where there is no note, the ketiv/qere template.",
        (
            "A file beside the book files",
            "A new near-Aleppo template wrapping the flagged text in the body text",
        ),
    ),
    Choice(
        "2026-09-16",
        _BEN,
        "The flags' names",
        "The two flag parameters have English names, `applied-and-flagged` and `flagged-not-applied`, and a site with no clause has a fixed English sentence as its value.",
        ("Hebrew names",),
    ),
    Choice(
        "2026-09-16",
        _BEN,
        "Which doubt-marked clauses are flagged",
        "Every clause that cites the codex with a doubt mark and gives a form MAM lacks, and every such clause whose quoted form ends in a question mark, is flagged `flagged-not-applied`, unless near-Aleppo already has the form.",
        (
            "Only the sites named when the flags were first planned",
            "Those clauses together with the agreeing clauses whose codex siglum is doubt-marked",
        ),
    ),
    Choice(
        "2026-09-16",
        _BEN,
        "Flags at Deuteronomy 5:23 and Leviticus 10:4",
        "Neither has a flag: the hataf at Deuteronomy 5:23 rests on the rule and on an undoubted clause, and Leviticus 10:4's question mark is a question and its answer, not a doubt mark.",
        (
            "A flag at Deuteronomy 5:23 alone",
            "A flag at both",
        ),
    ),
    Choice(
        "2026-09-16",
        _BEN,
        "The maqaf at Proverbs 3:30",
        "The maqaf policy left Proverbs 3:30's `א-כתיב!` clause to the pointed-ketiv work, which on 2026-09-24 gave near-Aleppo the clause's whole form, with a space where MAM has a maqaf before the template.",
        ("Removing the maqaf at once and flagging it",),
    ),
    Choice(
        "2026-09-16",
        _BEN,
        "The maqaf at Job 23:5",
        "At Job 23:5 near-Aleppo has a maqaf where MAM has a space, the first of the two forms the note gives the codex, the one with MAM's merkha, with no flag.",
        ("MAM's text, with the clause flagged",),
    ),
    Choice(
        "2026-09-16",
        _BEN,
        "Ezekiel 40:26's second ketiv/qere site",
        "The note's words `חסרה כאן הערת קרי` are read as denying a qere note, so near-Aleppo has the pointed ketiv there and no template.",
        ("The encoding kept and flagged",),
    ),
    Choice(
        "2026-09-16",
        _EDITORIAL,
        "The agreeing bang-marked clause at 1 Samuel 23:17",
        "The note at 1 Samuel 23:17, whose agreeing clause cites the codex with a bang, has an `applied-and-flagged` flag, as the other such clauses Ben had named do.",
        (),
    ),
    Choice(
        "2026-09-16",
        _EDITORIAL,
        "Where a silence flag goes when its template is in a note's target",
        "Where a ketiv/qere template flagged for the apparatus's silence stands in a note's target, the flag is on the enclosing note, which keeps every flag out of every note's target.",
        ("The flag on the ketiv/qere template itself",),
    ),
    Choice(
        "2026-09-23",
        _BEN,
        "The template names of notes that have MAM's target",
        "A `נוסח` or `מ:הערה-2` that has `מקרא על פי המסורה` has a template name specific to near-Aleppo, qualified wherever it is named as specific to near-Aleppo; the flags stay optional parameters.",
        ("MAM's names kept, with the parameter documented",),
    ),
    Choice(
        "2026-09-23",
        _EDITORIAL,
        "The template names of ketiv/qere templates that have a pointed ketiv",
        "A `כו״ק`, `קו״כ`, or `מ:כו״ק מיוחד` that has `כתיב מנוקד` keeps MAM's name, the added parameter being read as a branch beside MAM's parameters, whose meaning it leaves alone.",
        (),
    ),
    Choice(
        "2026-09-23",
        _BEN,
        "A codex form at a `קו״כ` target whose letters are the qere's",
        "At 2 Kings 14:7 near-Aleppo has the form the note gives the codex in the qere parameter of the `קו״כ`, the template kept; the forms with the ketiv's letters stayed pending that day.",
        (
            "Deferring every such form",
            "Settling the representation of a pointed ketiv at once",
        ),
    ),
    Choice(
        "2026-09-23",
        _BEN,
        "Numbers 22:5, where the note weighs two testimonies to the lost codex",
        "Near-Aleppo has MAM's defective spelling, as the note's conclusion does, and the note is flagged `flagged-not-applied` with its `א(ר)` clause.",
        (
            "Not applying the form, without a flag",
            "Applying the `א(ר)` form",
        ),
    ),
    Choice(
        "2026-09-23",
        _EDITORIAL,
        "A qualifier at the end of a list of sigla",
        "The build reads a qualifier such as `-כתיב` or `!` as applying only to the siglum it follows, as MAM-basics' sigil decoding counts it.",
        ("Reading it as distributing over the whole list",),
    ),
    Choice(
        "2026-09-23",
        _EDITORIAL,
        "Codex forms that quote the target without its final paseq glyph",
        "At Psalms 40:13 and Ruth 3:13 near-Aleppo has the paseq glyph that ends MAM's target, and counts the note's form, which quotes the word without it, as in place, the notes being about the hataf and the large nun.",
        (),
    ),
    Choice(
        "2026-09-23",
        _EDITORIAL,
        "Forms marked as errors that restore what a convention removes",
        "At Psalms 11:1 and 56:5 near-Aleppo has the ole and the yored on one letter, and at Ezekiel 28:22 the divine name with a holam on the first he, as the bang-marked forms the notes give the codex have them, applied and flagged.",
        (),
    ),
    Choice(
        "2026-09-23",
        _EDITORIAL_BEN_CONFIRMED,
        "The `שיטת-א` form at Song of Songs 8:4",
        "Near-Aleppo has the hataf patah on the first resh that the note's `שיטת-א` clause gives, at a verse where the codex is lost.",
        ("Reverting it",),
    ),
    Choice(
        "2026-09-23",
        _BEN,
        "How near-Aleppo has a pointed ketiv",
        "Where near-Aleppo has a pointed ketiv at a `כו״ק`, `קו״כ`, or `מ:כו״ק מיוחד`, it is a parameter added to MAM's template, which the build selects as the body text; MAM's parameters stay verbatim.",
        (
            "The template rewritten as MAM's `מ:קו״כ-אם-2`",
            "MAM's ketiv parameter overwritten",
            "A template specific to near-Aleppo",
        ),
    ),
    Choice(
        "2026-09-23",
        _BEN,
        "The name of the pointed-ketiv parameter",
        "The parameter is named `כתיב מנוקד`.",
        ("The name `pointed-ketiv`",),
    ),
    Choice(
        "2026-09-23",
        _BEN,
        "Which pointed ketivs near-Aleppo has",
        "This stage added the pointed ketivs MAM's notes give at two-sided templates. The approved frozen subset of 2026-10-02 adds inference at its accepted sites; one-sided sites remain later work.",
        (
            "Adding the one-sided sites",
            "Adding the inference of pointed ketivs from the qere",
        ),
    ),
    Choice(
        "2026-09-23",
        _BEN,
        "Codex forms under a plain `א` that have the ketiv's letters",
        "Near-Aleppo has every such form, its side read from its letters: as a pointed ketiv, or, at Deuteronomy 32:13, whose template went later on 2026-09-24, as plain text; Deuteronomy 28:27 and 29:22 have no flag.",
        (
            "Flagging Deuteronomy 28:27 and 29:22 `applied-and-flagged`, reading their heads' `-כתיב!` as distributing over the list",
            "Waiting for MAM-basics#290",
        ),
    ),
    Choice(
        "2026-09-23",
        _BEN,
        "The ZERO WIDTH NON-JOINER in Job 38:12's pointed ketiv",
        "Near-Aleppo has the codex form at Job 38:12 with the ZERO WIDTH NON-JOINER that MAM's note has between the tav and the he, so the body text has that character once, and the documentation says so.",
        ("Removing the character",),
    ),
    Choice(
        "2026-09-23",
        _EDITORIAL,
        "The maqaf in Isaiah 44:24's pointed ketiv",
        "Isaiah 44:24's pointed ketiv has the maqaf of the note's form, where MAM's ketiv has a space between the two words, the clause saying that the maqaf shows the two written words are read together.",
        ("The space MAM's ketiv has",),
    ),
    Choice(
        "2026-09-23",
        _BEN,
        "What renders the edition",
        "A copy of MAM-with-doc's renderer, pinned at one MAM-basics commit and changed only where near-Aleppo needs it, renders the edition; MAM's input must still give MAM-with-doc byte for byte.",
        (
            "Developing a separate renderer for near-Aleppo",
            "Deferring the edition to the move",
        ),
    ),
    Choice(
        "2026-09-23",
        _BEN,
        "What the documentation is",
        "Originally one page, written by a generator, every figure read from the build's asserted snapshot or computed from the data. The single-page structure was superseded by the division into topic pages on 2026-10-03; generation and figure checking remain.",
        (
            "A hand-written page",
            "Generated pages, one per topic",
        ),
    ),
    Choice(
        "2026-09-23",
        _BEN,
        "When the documentation is written",
        "The documentation describes near-Aleppo as it stands, with a section naming what is pending, and a mega-pipeline step regenerates and checks it.",
        (
            "No mega step yet",
            "Waiting for the inference of pointed ketivs",
        ),
    ),
    Choice(
        "2026-09-23",
        _BEN,
        "How the edition has the added parameters",
        "Each parameter near-Aleppo adds is one more line of its note, labelled with its name; MAM's target is rendered as MAM-with-doc renders MAM's text, and a flag's value as the JSON has it.",
        (
            "Flags as markers",
            "MAM's target only",
        ),
    ),
    Choice(
        "2026-09-23",
        _BEN,
        "The label of a note target that ends in a space",
        "The edition labels such a target without its trailing space, those from `מ:פסק` as `פסק` and those from `מ:מקף אפור` by their word; the verse text keeps the space.",
        ("A label showing the space, such as `{רווח}`",),
    ),
    Choice(
        "2026-09-23",
        _BEN,
        "Near-Aleppo's consumer notice",
        "Every book file's header has near-Aleppo's consumer notice, MAM's rules amended where near-Aleppo differs, and the page has the same notice.",
        ("MAM's notice kept until the move",),
    ),
    Choice(
        "2026-09-23",
        _BEN,
        "Which policies the documentation describes",
        "The documentation has a section on MAM's templates and one on each of near-Aleppo's conventions, beyond the items first listed for it.",
        ("The listed items alone",),
    ),
    Choice(
        "2026-09-23",
        _BEN,
        "The pages' stylesheets",
        "The documentation's stylesheet follows the repository's rules for generated HTML, and the edition keeps MAM-with-doc's stylesheet unchanged.",
        (
            "Those rules for both",
            "MAM-with-doc's stylesheet for both",
        ),
    ),
    Choice(
        "2026-09-23",
        _BEN,
        "The paseq glyph in the edition",
        "The edition has every paseq glyph as MAM-with-doc shows a legarmeh, a thin space and then the glyph, since near-Aleppo does not tell legarmeh from narrow-sense paseq.",
        ("The glyph as near-Aleppo has it",),
    ),
    Choice(
        "2026-09-23",
        _EDITORIAL,
        "How the edition's renderer knows which edition it renders",
        "There is no edition flag: what the edition needs is keyed on data MAM never has, the paseq display is one named render option, and what differs by page is passed in at the top.",
        (
            "A “what edition am I generating” flag passed around the renderer",
            "Such a flag held in a global",
        ),
    ),
    Choice(
        "2026-09-23",
        _EDITORIAL,
        "A note template in MAM's text of a note's target",
        "In the edition, the line of a note that gives MAM's text of its target shows a note template inside that text by its target alone: MAM's `מ:הערה-2` at five notes, and MAM's `מ:קו״כ-אם-2`, which MAM-with-doc shows as a note, at others.",
        ("The inner note's lines after MAM's text",),
    ),
    Choice(
        "2026-09-24",
        _BEN,
        "The documentation as a delta or a standalone reference",
        "Until the move, the documentation says what near-Aleppo changes or adds and links to MAM-parsed-plus's documentation for the rest; at the move it becomes a standalone reference built from shared generating code.",
        (
            "A standalone page now",
            "A delta permanently",
        ),
    ),
    Choice(
        "2026-09-24",
        _EDITORIAL,
        "A codex masorah note that is not a qere note",
        "Where MAM's note at a ketiv/qere word gives the codex's masorah note there, and that note is not a qere note, near-Aleppo reads the codex as having no qere note and has no ketiv/qere template, at Deuteronomy 32:13, Joshua 3:4, Zephaniah 2:9, and the second site of Ezekiel 40:24.",
        (
            "Leaving the sites as they were, some keeping the encoding and some flagged as sites where MAM's apparatus is silent about the codex",
            "Deciding only a subset of the sites with the same apparatus condition",
        ),
    ),
    Choice(
        "2026-09-24",
        _EDITORIAL,
        "The spelling at Ezekiel 40:24's second ketiv/qere site",
        "Near-Aleppo has the spelling the note gives the codex, with a yod before the final vav, which is MAM's parameter `3`, the pointed qere.",
        ("MAM's yod-less parameter `1`",),
    ),
    Choice(
        "2026-09-24",
        _EDITORIAL,
        "Zephaniah 2:9, where the note gives the codex no form",
        "Near-Aleppo has MAM's ketiv pointed by the transplant of the qere's pointing, the tie between two matchings broken toward the one that leaves no mark unplaced.",
        (
            "The ketiv unpointed",
            "The ketiv/qere encoding kept",
        ),
    ),
    Choice(
        "2026-09-25",
        _BEN,
        "The name of a `נוסח` that has MAM's target",
        "A `נוסח` that has `מקרא על פי המסורה` is named `נוסח למקרא על פי המסורה` in near-Aleppo.",
        (
            "The name `נוסח על המקרא על פי המסורה`",
            "The name `nusach-on-mam-text`",
        ),
    ),
    Choice(
        "2026-09-25",
        _BEN,
        "The name of a `מ:הערה-2` that has MAM's target",
        "A `מ:הערה-2` that has `מקרא על פי המסורה` is named `הערה-2 למקרא על פי המסורה` in near-Aleppo.",
        (
            "The name `הערה-2 על המקרא על פי המסורה`",
            "The name `hearah-2-on-mam-text`",
        ),
    ),
    Choice(
        "2026-09-25",
        _EDITORIAL,
        "A flag of two clauses in the edition",
        "In the edition, a flag whose value is two clauses of the note, joined as MAM joins a note's clauses, is two lines of the note, each labelled with the flag's name, as the note's clauses are two lines; this is at Isaiah 59:19.",
        ("One line holding both clauses",),
    ),
    Choice(
        "2026-09-25",
        _EDITORIAL,
        "The flag at 2 Samuel 13:33 in the edition",
        "The flag on the `כתיב ולא קרי` at 2 Samuel 13:33, which no note is about, is shown as a note on the ketiv and the maqaf after it, labelled with the ketiv, whose one line is the flag.",
        ("A marker in the verse text beside the ketiv",),
    ),
    Choice(
        "2026-09-25",
        _EDITORIAL,
        "A scroll-difference note inside a note, in the edition",
        "Where a `נוסח למקרא על פי המסורה` holds a `הערה-2 למקרא על פי המסורה`, each has MAM's text of the target, the same text; the edition has the two as one note, as MAM-with-doc shows a `נוסח` that holds a `מ:הערה-2`, with one line of MAM's text.",
        ("A line of MAM's text for each",),
    ),
    Choice(
        "2026-10-02",
        _BEN,
        "Frozen source-only pointed-ketiv inference",
        "An approved subset of singleton source-only predictions is imported from an immutable snapshot after note-derived readings. Broader warnings and ownership evidence remain in a separate source archive. Existing note pointings take priority; no source-attribution field is added to a template. Later research does not change this snapshot.",
        (
            "Requiring every broader provenance warning to be absent",
            "Running the evolving research algorithm during production builds",
            "Importing unresolved ownership nodes",
        ),
    ),
    Choice(
        "2026-10-05",
        _BEN,
        "The leading orphan qubuts at Lamentations 4:16",
        "Near-Aleppo retains the leading orphan qubuts on an artificial alef carrier. MAM's apparatus records that mark in the ketiv entries for Sassoon 1053 and Cambridge Add. 1753, and its absence in the Leningrad entry. Where Aleppo is missing, the choice aims at an Aleppo-flavored Masoretic consensus; it is an editorial choice and makes no claim of fresh Aleppo manuscript evidence.",
        (
            "Omitting the leading orphan qubuts, following the Leningrad entry in MAM's apparatus",
        ),
    ),
    Choice(
        "2026-10-05",
        _BEN,
        "The final-nun dagesh at Isaiah 54:16",
        "Near-Aleppo retains the dagesh on the final nun. Ben reported that he inspected an Aleppo image that day and saw the dot. This observation is attributed to Ben. This unusual final-nun dagesh is a case-specific choice and establishes no general legality rule.",
        ("Omitting the dagesh on the final nun",),
    ),
    Choice(
        "2026-10-05",
        _BEN,
        "The later GV carrier extension",
        "Ben's GV extension of 2026-10-05 accepts the artificial VAV + HOLAM carrier tagged carrier=holam-male-vav in the template specific to the near-Aleppo dataset, `ניקוד בלי אות`. This records the chosen holam-male meaning; the original GA shape remains accepted. JSON stores the carrier payload, and the example edition displays it between double guillemets.",
        (
            "Converting the chosen GV carrier to ALEF + HOLAM, losing its holam-male meaning",
        ),
    ),
)


def section(numbers):
    del numbers  # the rows state no figure
    dates = [choice.date for choice in _CHOICES]
    if dates != sorted(dates):
        raise AssertionError("the choices are not oldest first")
    rows = [
        [
            [mb_html.bold(_prose(choice.topic + ".")), " ", *_prose(choice.chosen)],
            _alternatives(choice.alternatives),
        ]
        for choice in _CHOICES
    ]
    return [
        mb_html.heading_level_2(SECTION[1], {"id": SECTION[0]}),
        mb_html.para(
            "Many of near-Aleppo's choices could reasonably have gone another way."
        ),
        table(
            ["What was chosen", "Alternatives not taken"],
            rows,
            [None, None],
        ),
        mb_html.para(
            [
                "The carrier and guillemet choices describe the raw JSON and "
                "this example edition. Other editions can make late display "
                "choices while retaining the orphan marks' semantics; see ",
                link(
                    "GAV notation and display in practice",
                    "reading-json.html#gav-display",
                ),
                ".",
            ]
        ),
    ]


def _alternatives(alternatives):
    if not alternatives:
        return "None recorded"
    if len(alternatives) == 1:
        return _prose(alternatives[0])
    return mb_html.unordered_list([_prose(item) for item in alternatives])


def _prose(text):
    """``text`` as page contents: each name between backticks as Hebrew, isolated, or
    else as code, and each Hebrew run of the rest isolated."""
    parts = text.split("`")
    if len(parts) % 2 != 1:
        raise AssertionError(f"unpaired backtick in {text!r}")
    out = []
    for index, part in enumerate(parts):
        if index % 2:
            out.append(he_name(part) if _HEBREW_LETTER.search(part) else code(part))
        elif part:
            out.extend(isolated(part))
    return out
