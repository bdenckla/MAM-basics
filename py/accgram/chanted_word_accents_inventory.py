"""Yeivin's and Breuer's inventories, Ben's allowances, and the whitelist derived from them.

Declarative tables: the two books' inventories, transcribed from their sources, and Ben's
allowances for what neither book names.  The survey in ``chanted_word_accents`` checks each
table against MAM and sets it beside the measurement; its module docstring is the design of
this module too.  The whitelist ``classify_verse`` reads, ``NAMED_TOKEN_SEQUENCES`` and
``_ALLOWANCE_INDEX``, is derived here, and each derivation raises on a conflict between the
tables.
"""

from __future__ import annotations

from dataclasses import dataclass

from accgram import accent_marks as am

# --- Yeivin's prose inventory -------------------------------------------------
#
# Transcribed from the FULL OCR of the book at
# ``../masorah-books/books/itm/md-export-of-docx/`` -- that repo was ``yeivin-itm`` until it was
# renamed on 2026-07-31 -- not from
# the partial adaptation at ``../al-hatorah/py/itm/``, which does not carry all of these sections.
# Each ``quote`` is Yeivin's own wording, so it keeps his romanizations: he spells tifxa with a
# dotted t and a dotted h, and munax with a dotted h, where the rest of this repo spells xet with
# an x.  The spellings themselves stand in the quote strings below, which are values and not
# comments.
#
# ``sequences`` are the scanner's own leaf names, which is what makes an entry checkable: the
# measured hits with that token sequence are the entry's measured set.  ``verses`` is Yeivin's
# closed list where he gives one.  ``exact`` says whether the two sets are expected to be equal;
# where they are not, his list must still be CONTAINED in the measurement, and the surplus is
# reported as ``measured_beyond_yeivin`` rather than passed over.

_ITM = "Yeivin, Introduction to the Tiberian Masorah"


@dataclass(frozen=True)
class YeivinEntry:
    section: str
    names: str
    stated_count: str
    quote: str
    sequences: tuple[str, ...] = ()
    verses: tuple[str, ...] = ()
    exact: bool = False
    note: str = ""


YEIVIN_ENTRIES: tuple[YeivinEntry, ...] = (
    YeivinEntry(
        section="§209",
        names="silluq takes one conjunctive, and no secondary accent",
        stated_count="(a rule, not a count)",
        quote=(
            "Silluq can only be preceded by one conjunctive, and this is merka."  # translit-ok
        ),
        note=(
            "Here so that a silence is checkable rather than assumed. Nothing in this"
            " inventory names a secondary merkha in a silluq's chanted word, and §209 with"
            " §210 is the pair that makes that evidence: §209 is the whole statement of"
            " silluq's conjunctives and adds no secondary, and §210 is the only section"
            " that gives silluq a second mark, which is the mayela. §210's stated"
            " condition excludes the one MAM chanted word at issue on its own terms --"
            " 'In these cases silluq has neither tipexa nor a conjunctive before it' --"
            " where Song 8:6 has the tipexa on אש, one chanted word earlier. Searched over"
            " the full OCR on 2026-08-03, section by section: of the thirteen that name a"
            " secondary accent with a given disjunctive, silluq is in one. Two near misses"
            " are not it, §212's exceptional Micah 6:3, where a merkha is the only accent"
            " between etnaxta and silluq but stands on a chanted word of its own, and"
            " §373's poetic metigah, where the metigah is the secondary mark and the merkha"
            " an ordinary servus. Breuer is silent in the same place: CoS Ch. 3 §39 gives"
            " the silluq's servant across two separate words and §40, the same-word"
            " section, is the mayela's alone, both pinned in masorah-books'"
            " check_cos_claims.py. So ca8:6 שלהבתיה stands in ``mam_residue`` unnamed by"
            " either book -- and it is the one atomic merkha-with-silluq chanted word in"
            " any of the three corpora, which all three have. Issue wlc-utils#86."
        ),
    ),
    YeivinEntry(
        section="§210",
        # "The mayela", never "the mayela tipexa" -- mayela is the name for what would otherwise
        # be a tipexa there, as ``maqaf_nonfinal_accents``' ANFA-reason-(a) bullet sets out.  Yeivin's
        # own quote below is where the reader learns the sign's shape.
        names="the mayela with silluq",
        stated_count="in five places",
        quote=(
            "In five places, the word bearing silluq has, in addition, a secondary accent"
            " like ṭifḥa in form."
        ),
        sequences=("mayela silluq",),
        verses=("lv21:4", "nu15:21", "is8:17", "ho11:6", "1c2:53"),
        exact=True,
        note=(
            "Yeivin adds that the Masorah treats the sign as a conjunctive under the name"
            " mayela, and that the same sign occurs with etnaxta (§216)."
        ),
    ),
    YeivinEntry(
        section="§215",
        names="munax with etnaxta",
        stated_count="in two cases",
        quote=(
            "In two cases munaḥ is used as a secondary accent in the same word as atnaḥ,"
            " marked on an open, syllable suitable for gaʿya (#326)."
        ),
        sequences=("munax atnax",),
        verses=("2s12:25", "1c5:20"),
        exact=True,
    ),
    YeivinEntry(
        section="§216",
        names="the mayela with etnaxta",
        stated_count="in ten or eleven cases",
        quote=(
            "In ten or eleven cases in the Bible, a sign of the same form as ṭifḥa appears"
            " as a secondary accent on the same word as atnaḥ."
        ),
        sequences=("mayela atnax",),
        verses=(
            "gn8:18",
            # The OCR line reads "בשבעת יכם 8:26 2 Nu", which is Numbers 28:26 with the 28
            # broken across the reference: בשבעתיכם stands there and nowhere in Numbers 2.
            "nu28:26",
            "2k9:2",
            "je2:31",
            "ek7:25",
            "ek10:13",
            "ek11:18",
            "da4:9",
            "da4:18",
            "ru1:10",
            "2c20:8",
        ),
        exact=True,
        note=(
            "The count is Yeivin's own 'ten or eleven'; his list has eleven, of which he"
            " says of Ezekiel 10:13 that mayela is not used there in some early"
            " manuscripts."
        ),
    ),
    YeivinEntry(
        section="§219",
        names="munax-zaqef -- a fourth variant of the zaqef melody",
        stated_count="in many cases",
        quote=(
            "In many cases also munaḥ is marked as a secondary accent on the same word as"
            " zaqef and this combination is considered as a fourth variant of the zaqef"
            " melody."
        ),
        sequences=("munax zaqef",),
        note=(
            "§221 gives the conditions: the combination is used when the zaqef word"
            " includes an open syllable suitable for gaʿya which is not the first syllable."
            " By far the largest class here, and open, so there is no list to check against."
        ),
    ),
    YeivinEntry(
        section="§223",
        names="metigah-zaqef",
        stated_count="(no count given)",
        quote=(
            "If the zaqef is not preceded by pashṭa, and if the word bearing zaqef contains"
            " a closed syllable which is separated from the stress syllable by a full"
            " vowel--or at least by a vocal shewa, and if this closed syllable is not the"
            " first in the word, the methigah-zaqef is used."
        ),
        note=(
            "Invisible to this survey by construction: the scanner fuses qadma...zaqef into"
            " one METHIGAZAQEF token, so a metigah-zaqef chanted word has one accent token,"
            " not two. The fuse crosses a maqaf, as this section's leading example Ex 35:9"
            " ואבני־שהם requires, and stops at a space, on this section's 'the word bearing"
            " zaqef' and CoS Ch. 5 §4's 'A methiga will appear in the word of the small"
            " zakef'. So a fused pair is always one chanted word, and"
            " ``crossing_a_chanted_word_boundary`` is 0 in all three corpora -- a lint on the"
            " scanner rather than a measurement of the corpus. The token count is under"
            " ``methigazaqef`` in each corpus."
        ),
    ),
    YeivinEntry(
        section="§233",
        names="merkha with tipexa -- a secondary merkha in the tipexa's chanted word",
        stated_count="in 8 cases",
        quote=(
            "In 8 cases merka occurs as a secondary accent on the same word as ṭifḥa,"  # translit-ok
            " generally on an open syllable suitable for gaʿya."
        ),
        sequences=("merkha tipexa",),
        verses=(
            "lv23:21",
            "2k15:16",
            "je8:18",
            "ek36:25",
            "ek44:6",
            "da5:17",
            "ca6:5",
            "1c15:13",
        ),
        note=(
            "Yeivin's eight are the cases where the merkha is a SECONDARY accent, and all"
            " eight have both marks on ONE atom. The measurement is wider, because it"
            " counts any chanted word with both marks -- including four compounds whose"
            " non-final atom has a merkha of its own, a gaʿya after it and then §357's"
            " maqaf. Those four are not §233 cases and are not §293's habit either; see"
            " ``maqaf_after_gaya``."
        ),
    ),
    YeivinEntry(
        section="§236",
        names="munax with revia",
        stated_count="in five cases",
        quote=(
            "In five cases munaḥ appears as a secondary accent in the same word as revia."
        ),
        sequences=("munax revia",),
        verses=("gn45:5", "ex32:31", "zc7:14", "ec4:10", "da1:7"),
        exact=True,
    ),
    YeivinEntry(
        section="§241",
        names="mahapakh with pashta (Yeivin spells the accent mehuppak)",  # translit-ok
        stated_count="in five cases",
        quote=(
            "In five cases mehuppak appears as a secondary accent on the same word as"  # translit-ok
            " pashṭa. It is marked on an open syllable suitable for gaʿya, which happens to"
            " be formed, in all cases, by the prefixed particle -ש."
        ),
        sequences=("mahapakh pashta",),
        verses=("ca1:7", "ca1:12", "ca3:4", "ec1:7", "ec7:10"),
        note=(
            "This is the section ``maqaf_nonfinal_accents`` used to cite for a secondary"
            " mahapakh in a TEVIR's chanted word; the pairing is with pashta, and the tevir"
            " entry never fired in any corpus. The three MAM chanted words beyond Yeivin's"
            " five all have the mahapakh on a non-final atom and the pashta on the last --"
            " the same shape as §233's surplus, and not the prefixed ־ש his five are about."
            " All three have a gaʿya after that mahapakh and then §357's maqaf, and Yeivin"
            " names one of them, Isaiah 59:16, at §357 itself; Breuer names another,"
            " Isaiah 63:5, at CoS Ch. 1 §43. See ``maqaf_after_gaya``."
        ),
    ),
    YeivinEntry(
        section="§244",
        names="both servi of pashta on one chanted word",
        stated_count="in eight places",
        quote=(
            "In eight places the two servi of pashṭa are marked on the same word, the"
            " second of them marked as a secondary accent generally on an open syllable"
            " suitable for gaʿya (#326)."
        ),
        sequences=("qadma mahapakh", "qadma merkha", "munax mahapakh"),
        verses=(
            "lv25:46",
            "nu20:1",
            "dt8:16",
            "ek43:11",
            "lm4:9",
            "da3:2",
            "er7:24",
            "2c35:25",
        ),
        note=(
            "Not one token sequence but three, because which pair of servi appears is"
            " settled by §240 and §242 (mahapakh or merkha first before pashta; munax or"
            " azla second), and the second servus tokenizes as qadma rather than azla"
            " wherever no geresh follows. ``mam_measured`` is therefore the union of the"
            " three sequences and is NOT a count of §244 cases: those three pairs also"
            " serve other disjunctives, and the surplus under ``measured_beyond_yeivin``"
            " is where they do. What is checked here is that all eight of Yeivin's"
            " chanted words are measured. §245 adds the one where the two servi share a"
            " base letter, Ezekiel 20:31, which the scanner fuses into a single"
            " mahapakh!qadma token and this survey therefore does not see as two."
        ),
    ),
    YeivinEntry(
        section="§253",
        names="merkha-tevir -- a secondary merkha in the tevir's chanted word",
        stated_count="in some hundred cases",
        quote=(
            "In some hundred cases merka is marked as a secondary accent on the same word"  # translit-ok
            " as tevir, (Of the secondary accents, the use of munaḥ-zaqef, #221, is more"
            " frequent)."
        ),
        sequences=("merkha tevir",),
        note=(
            "The measured count falls well short of Yeivin's hundred, and §254 says why:"
            " 'Already in L gaʿya occurs in most of the cases where merka is expected.' A"  # translit-ok
            " meteg is not an accent and emits no token, so wherever the Leningrad Codex"
            " has one the chanted word has a single accent token here. This is also the"
            " section ``maqaf_nonfinal_accents`` should have cited for merkha-tevir."
        ),
    ),
    YeivinEntry(
        section="§256",
        names="both servi of tevir on one chanted word",
        stated_count="in eight cases",
        quote=(
            "In eight cases the two servi of tevir are marked on the same word, with the"
            " azla on an open syllable suitable for gaʿya."
        ),
        sequences=("qadma darga",),
        verses=("jb1:15", "jb1:16", "jb1:17", "jb1:19", "ne11:7", "2c17:8"),
        exact=True,
        note=(
            "The tevir's counterpart of §244, and the section that names Job's four"
            " prose-frame ואמלטה -- his own example, cited as 'Job 1:15, 16, 17, 19'."
            " Six of his eight are listed here. The other two, Isaiah 30:16 ותאמרו and"
            " Isaiah 32:15 יערה, have a merkha as the second servus rather than a darga,"
            " so they measure as ``qadma merkha``, a sequence §244 already claims; a"
            " token sequence is claimed by one section only, so they are recorded in this"
            " note instead of in the list. The six listed are the whole of MAM's"
            " ``qadma darga``."
        ),
    ),
    YeivinEntry(
        section="§268",
        names="azla-geresh on one chanted word",
        stated_count="often",
        quote=(
            "Azla is often marked as a secondary accent on the word bearing geresh. This"
            " occurs under conditions similar to those governing the marking of munaḥ on"
            " the word bearing zaqef, or merka on the word bearing tevir (#221, 253)."  # translit-ok
        ),
        sequences=("azla geresh",),
        note=(
            "The second-largest class measured, and the one the earlier survey's named"
            " configurations left out altogether."
        ),
    ),
    YeivinEntry(
        section="§276",
        names="munax in the chanted word of a pazer",
        stated_count="in one case",
        quote=(
            "In one case, ... (Gen 50:17) the servus munaḥ is marked as a secondary accent"
            " on the word bearing pazer."
        ),
        sequences=("munax pazer",),
        verses=("gn50:17",),
        exact=True,
    ),
    YeivinEntry(
        section="§302",
        names="a maqaf compound is one unit for these rules",
        stated_count="(a rule, not a count)",
        quote=(
            "From the point of view of the accentuation, words joined by maqqef are"
            " considered as a single unit, and are treated so in the marking of"
            " conjunctives, secondary accents, and gaʿya."
        ),
        note=(
            "The warrant for measuring atomic chanted words and maqaf compounds together"
            " rather than as two phenomena. Yeivin's own illustration is אל־האשה taking"
            " munax-zaqef precisely because the maqaf makes the two atoms one unit."
        ),
    ),
    YeivinEntry(
        section="§354",
        names="gaʿya after the accent, on a word with penultimate stress",
        stated_count="(a rule, not a count)",
        quote=(
            "Gaʿya is similarly sometimes used on the last syllable of a word with"
            " penultimate stress if it ends with a guttural and the following word begins"
            " with lamed or nun."
        ),
        note=(
            "Yeivin's three examples are Ruth 1:21, 1 Kings 2:8 and Ezekiel 1:4 ונגה לו,"
            " and he writes all three with a SPACE. MAM has a maqaf after the gaʿya at"
            " Ezekiel 1:4, which is the only reason that compound reaches this survey."
            " See ``maqaf_after_gaya``."
        ),
    ),
    YeivinEntry(
        section="§357",
        names="maqqef after gaʿya",
        stated_count="(a rule, not a count)",
        quote=(
            "In some MSS maqqef is marked -- sometimes consistently, sometimes"
            " sporadically -- after a word marked with gaʿya after the accent. ... The"
            " purpose of this maqqef is to indicate that, even though gaʿya is marked"
            " after the accent, so that the reading of that syllable must be slowed down,"
            " the word must be joined to the following word, and no break should be made"
            " between them."
        ),
        note=(
            "The section that says what thirteen of MAM's twenty-two compounds with their"
            " accents split across atoms are. Yeivin's four examples carry a manuscript"
            " apiece -- Jeremiah 49:23 in C, Numbers 24:22 in S, Isaiah 59:16 in A and C,"
            " Lamentations 5:6 in L3 -- and Isaiah 59:16 is one of the thirteen. A hit of"
            " this kind IS a chanted word, on the only test there is for one -- a maqaf is"
            " written in it -- and it is counted as one here. What §357 settles is where the"
            " second accent token comes from: the non-final atom keeps the accent it has,"
            " the gaʿya written after that accent having had to be marked, so the token is"
            " not a secondary accent of the kind §§233 and 241 are about."
            " WHAT THE MAQAF SIGNIFIES IS NOT SETTLED, by either book, and this note does"
            " not settle it either. Yeivin's 'the word must be joined to the following word'"
            " reads as denying a pause rather than as making one chanted word with one"
            " accent: he writes these very compounds with a SPACE at §354 -- Ezekiel 1:4"
            " ונגה לו, Ruth 1:21 הרע לי, 1 Kings 2:8 ואשבע לו -- where a servant standing on"
            " one chanted word before its mafsik on the next is the ordinary relation."
            " Breuer CoS Ch. 1 §43 says outright that 'different views have been expressed'"
            " about this maqaf and leaves it out of the book, calling the mark a mesharet;"
            " Ch. 9 §37 points the other way, that an ordinary-order mark cannot stand in a"
            " hyphenated word, which would make the mark secondary and the compound one"
            " chanted word after all. Neither book squares the two. None of that bears on"
            " the NAME: what makes a chanted word here is the maqaf on the page, not an"
            " adjudication between §43 and §37. See ``maqaf_after_gaya``."
        ),
    ),
)


# --- Breuer, where he covers the same ground -----------------------------------
#
# Read off the full markdown export at ``../masorah-books/books/cos/md-export-of-docx/``, and
# pinned there by ``py/main_ocr.py cos-check-claims``.  Only four sections, because only four
# are load-bearing for what this survey cannot otherwise say: the one that defines the maqaf of
# ``maqaf_after_gaya``, the one that gives the tipexa's same-word servant, the one that says
# a secondary mark leaves a maqaf standing, and -- added 2026-08-18 -- Ch. 3 §2, which names
# ne8:7 by verse and is the only entry here that reaches a measurement.  Each ``quote`` keeps
# Breuer's romanizations, which
# differ from this repo's for most of the accent names; the spellings themselves stay in the
# quote strings, which are values and not comments.  His English names the maqaf as a hyphen far
# more often than by any transliteration of it, and never by either spelling this repo uses --
# so grep the translator's spelling and the Hebrew as well, or the topic looks absent.

_COS = "Breuer, The Cantillation of Scripture"


@dataclass(frozen=True)
class BreuerEntry:
    """One section of Breuer's, and -- where it gives a closed list -- what MAM must measure.

    ``sequences`` and ``verses`` are set only where the section NAMES a token sequence and lists
    every place it occurs, which of the four entries is true of Ch. 3 §2 alone.  Where they are
    set, ``breuer_notes`` asserts MAM against them and ``mam_residue`` sets the section's chanted
    words aside, so the group and the entry cannot part company.  The other three stay
    record-only, and for two different reasons: Ch. 1 §43 and Ch. 9 §37 describe a maqaf rather
    than a pair of accents, and Ch. 3 §28's eight are already ITM §233's eight, so that pair
    reaches ``NAMED_TOKEN_SEQUENCES`` through Yeivin and needs nothing here.
    """

    section: str
    names: str
    quote: str
    note: str = ""
    sequences: tuple[str, ...] = ()
    verses: tuple[str, ...] = ()


BREUER_ENTRIES: tuple[BreuerEntry, ...] = (
    BreuerEntry(
        section="Ch. 1 §43",
        names="the maqaf written after a servant that has a gaʿya on its last syllable",
        quote=(
            "In ancient manuscripts there sometimes appears a makaf in other"  # translit-ok
            " circumstances. A makaf of this type appears sometimes after a word"  # translit-ok
            " cantillated with a mesharet, which is accentuated mile'eil, and a ga'aya"  # translit-ok
            " usually appears on its last syllable; e.g.: ותושע־לי (Isa. 63:5). About the"
            " significance of this makaf different views have been expressed. But since"  # translit-ok
            " this makaf does not appear in a regular manner in most of the manuscripts,"  # translit-ok
            " and it is apparently left to the discretion of every nakdan, and since there"
            " is no trace of it in the accepted editions of Scripture, we shall not discuss"
            " it in this book."
        ),
        note=(
            "Breuer defines the configuration exactly as the measurement finds it -- an"
            " ordinary SERVANT, a word accented on its penultimate syllable, a gaʿya on"
            " its last -- names Isaiah 63:5, which is one of the thirteen, and then puts"
            " the whole class outside his book. Yeivin's ITM §357 is the same maqaf. Two"
            " things follow: neither book's inventory of secondary accents is where these"
            " belong, and Breuer's 'no trace of it in the accepted editions' is a"
            " divergence from MAM, which has thirteen of them."
        ),
    ),
    BreuerEntry(
        section="Ch. 3 §2",
        names="the legarmeh's servant in its own chanted word",
        quote=(
            "In one place, the servant of the legarmeih appears with it in its word - in"
            " a syllable fit for a light ga'aya: ... (Nehem. 8:7) ... The servant is a"
            " merkha according to the rule explained above, § 1."
        ),
        note=(
            "Breuer's closed list of one is MAM's one, and ``breuer_notes`` asserts it"
            " rather than reporting it: MAM has exactly ne8:7 for this pair, and the"
            " build raises otherwise. ITM has nothing of the kind. Yeivin cites Ne 8:7 at"
            " §279.4 only as one of the two places a legarmeh stands before a pazer; his"
            " §§281-282 give legarmeh one or two servi and put them on PRECEDING chanted"
            " words; and his inventory of secondary accents -- §§221, 223, 233, 241, 253,"
            " 268, and §276's lone munax with a pazer at Gen 50:17 -- has no legarmeh"
            " entry at all. So this pair is named by Breuer alone, and that is why ne8:7"
            " takes no entry in MAM_ALLOWANCES: that table is for what neither book"
            " names, and §2 names this. Ben's decision, 2026-08-18, on the ground §10 of"
            " doc/PLAN-two-accents-on-one-chanted-word.md dissolved ek16:12 on."
            " ISSUE #215 IS WHY THE SECTION WENT UNREAD until then. MAM tokenized no"
            " legarmeh anywhere until that fix landed, so ne8:7 measured as merkha munax"
            " and there was no merkha-legarmeh to look up; the search of Chapter 3 run on"
            " 2026-08-03 read §20, §28, §39 and §40 -- the four masorah-books'"
            " cos-check-claims pins -- and stopped short of §2, which opens the chapter."
            " Breuer also answers what #185 asks of the mark, calling it the servant"
            " merkha in a syllable fit for a light gaʿya rather than a gaʿya itself."
            " #185 stays open, weighing manuscripts against printed editions, and this is"
            " one voice in that; if it ever settles on a meteg this entry's list empties"
            " and the assertion above fires, which is the intended way to be told."
        ),
        sequences=("merkha legarmeh",),
        verses=("ne8:7",),
    ),
    BreuerEntry(
        section="Ch. 3 §28",
        names="the tipexa's servant in its own chanted word",
        quote=(
            "In eight places, the servant of tipekha appears with it in its word. ... The"  # translit-ok
            " servant is merkha - according to the ordinary order of the cantillation"
            " marks (above, §26); and it appears in a syllable fit for a light ga'aya or"  # translit-ok
            " in a syllable fit for the ga'aya of the big vowel."  # translit-ok
        ),
        note=(
            "Breuer's eight are Yeivin's eight at ITM §233, and his criterion says why the"
            " four beyond them are not of this kind: his servant stands on a syllable fit"
            " for a gaʿya, where each of the four instead has its accent on the atom's own"
            " stress with the gaʿya after it."
        ),
    ),
    BreuerEntry(
        section="Ch. 9 §37",
        names="a secondary mark does not cancel the maqaf; an ordinary one does",
        quote=(
            "A cantillation mark, which follows the regular order of the cantillation"
            " marks, cannot appear in a word joined by hyphen to the next one; therefore,"
            " if a hyphenated word receives a cantillation mark, the hyphenation is"
            " immediately cancelled. ... Therefore, we find that all the secondary"
            " cantillation marks in the 21 books appear even in a hyphenated word, and the"
            " hyphen is never cancelled after them. So with the me'ayla that serves before"  # translit-ok
            " a siluk or ethnakhta; e.g.: וקויתי־לו (Isa. 8:17), ויצא־נח (Gen. 8:18); and"  # translit-ok
            " so, too, with the methiga that appears in the word of the small zakef."  # translit-ok
        ),
        note=(
            "The rule that partitions the split compounds, and the two examples Breuer"
            " gives are two of the nine MAM compounds that have no gaʿya after the"
            " non-final accent. At the other thirteen this rule and Ch. 1 §43 pull against"
            " each other, and Breuer does not square them: §37 would make the mark"
            " secondary and the compound one chanted word, where §43 declines to say what"
            " the mark is. ``maqaf_after_gaya`` reports that as a dispute and settles"
            " nothing by it -- the partition there is by the writing, a gaʿya between the"
            " non-final atom's accent and the maqaf."
        ),
    ),
)


# Every token sequence a section of Breuer's names outright, read straight off the entries above
# so ``mam_residue``'s group and the entry that licenses it cannot part company.  Yeivin's
# sections reach the checker through ``NAMED_TOKEN_SEQUENCES``; Breuer's do not, and this is
# deliberately not that table -- ``mam_residue`` is closed against ``YEIVIN_ENTRIES`` alone and
# stays so, and what this does is set a group aside INSIDE the residue, the way ITM §357's
# maqaf-after-gaʿya compounds are set aside, without taking anything out of the total.
BREUER_NAMED_SEQUENCES: frozenset[str] = frozenset(
    seq for e in BREUER_ENTRIES for seq in e.sequences
)


# --- Ben's ruling, where neither book names what MAM has ----------------------
#
# §6 decision 5 of ``doc/PLAN-two-accents-on-one-chanted-word.md``, settled with Ben on
# 2026-08-03: MAM's divergences from Yeivin's and Breuer's rules are recorded, and are
# grammatical for the time being.  A chanted word below is therefore named by a RULING and not
# by a section, and the two are deliberately not fed from one table, so that a reader can see
# which entries are transcribed from Yeivin and which are Ben's.
#
# THE RULING DECIDES VERDICTS AND RETIRES NO MEASUREMENT.  "All divergences ... should continue
# to be recorded, for possible future return to (for further research)" is the other half of it.
# So ``mam_residue`` is computed off ``YEIVIN_ENTRIES`` alone and this table does not reach it:
# ca8:6 stays in the residue, under ``left_over_after_all_three``, exactly where it stood before the
# ruling.  ``wlc_chanted_word_residue_page`` keys on ``NAMED_TOKEN_SEQUENCES`` alone for the same
# reason -- the ruling covers MAM, and WLC's residue is a different set.
#
# CALL THESE ALLOWANCES.  The plan's phrase is "per-verse exception"; ``MamAllowance`` is that
# same thing under a name no reader can take for a Python exception.
#
# KEYED ON THE MARK RUN PLUS THE TOKEN SEQUENCE, NEVER ON A VERSE REFERENCE -- the mechanism the
# plan's §10 settled (Ben, 2026-08-03), and the shape ``lexical_validation``'s
# ``_WHITELISTED_SAME_LETTER`` already has, with its verses in a comment.
# ``classify_verse(body, tokens)`` has no verse reference and does not grow one: a mark run says
# what the chanted word HAS, which is what decision 1 asked a whitelist to name it by, and it is
# far tighter than the token sequence alone.  ``verses`` is the survey's differential check and
# nothing else -- ``mam_allowances`` asserts that MAM has each allowance in exactly those places
# and raises on drift, the shape Yeivin's closed lists already have -- and no flagging path
# reads it.
#
# THE MARK RUN IS BUILT FROM NAMED CONSTANTS, not typed as Hebrew: a key that has to be read
# mark by mark is one a reader can check, and a mistyped one would match nothing at all.
#
# THE FIVE TELISHA-GEDOLA WORDS ARE DELIBERATELY NOT NAMED HERE.  Phase 4 of the plan asked
# whether they should be, "so that the whole whitelist reads out of one place", and settled it no
# on 2026-08-17.  They are the words ``lexical_validation``'s ``_WHITELISTED_SAME_LETTER`` spares
# -- a telisha gedola and a geresh-family mark on ONE letter -- and an entry here would put one
# rule in two places rather than the whole whitelist in one.  Four measurements say so, each
# taken 2026-08-17 and each re-derivable by running ``survey-chanted-word-accents`` and reading
# the three corpora's occurrences:
#
#   * That whitelist is ORDER-LESS by design, a frozenset of frozensets, on the stated ground
#     that the order of two accents stacked on one letter is not meaningful.  A key here is a
#     token SEQUENCE, which is ordered, so an entry would have to spell each pair twice and would
#     restate in an ordered form a legality that was decided without order.
#   * The corpora do write them in both orders.  MAM has ``geresh telishagedola`` at ek48:10 and
#     ``gershayim telishagedola`` at lv10:4, where WLC and UXLC have ``telishagedola geresh`` and
#     ``telishagedola gershayim``.  An entry taken from MAM would therefore not describe what the
#     flagging path meets, that path reading WLC and the printed-Decalogue strands.
#   * A mark run does not travel either, which is the sharper half of the same point: WLC's
#     zp2:15 run has the ``]C]c`` note markers MAM's lacks, and WLC's 2k17:13 has the geresh
#     muqdam codepoint where MAM and UXLC have a plain geresh.  ca8:6 is the case where the mark
#     run IS the same in all three corpora, which is why §10 of the plan could settle the
#     mechanism on it.
#   * WLC's telisha-containing hits are not the same set.  je36:11 ``telishagedola revia`` and
#     js2:1 ``munax telishagedola`` have no same-letter pair in them at all, so an entry keyed on
#     the token sequence would sweep in two chanted words ``lexical_validation`` does not
#     whitelist and nothing has ruled on.
#
# What a reader is owed instead is a pointer, and there are two: this paragraph, and
# ``mam_residue``'s ``already_documented_elsewhere``, which says where the five are accounted
# for.
#
# NE8:7 IS NOT NAMED HERE EITHER, THOUGH THE PLAN SAYS IT WOULD BE.  §10 of
# ``doc/PLAN-two-accents-on-one-chanted-word.md`` held ne8:7 ושר֥בי֣ה on issue #215 and said its
# allowance would be written here against whatever sequence MAM had once that was fixed.  #215
# was fixed on 2026-08-18 and MAM's sequence turned out to be ``merkha legarmeh`` -- and Breuer
# CoS Ch. 3 §2 names exactly that, at exactly that verse, as the one place a legarmeh's servant
# appears in its own chanted word.  So no allowance is owed and none is written: this table is
# for what NEITHER book names, and §2 names this.  Ben's decision, 2026-08-18, on the ground §10
# itself dissolved ek16:12 on when ITM §357 turned out to account for that one.  The entry lives
# in ``BREUER_ENTRIES`` instead, with a closed list of one that ``breuer_notes`` asserts against
# MAM, and ``mam_residue`` sets the chanted word aside under
# ``accounted_for_by_breuer_ch3_s2`` while still counting it.  #215 is also why nobody had read
# §2: while MAM tokenized no legarmeh anywhere, ne8:7 measured as ``merkha munax`` and there was
# no ``merkha legarmeh`` to look up.
#
# So ``MAM_ALLOWANCES`` has one entry and not two, and that is the finished state of the plan
# rather than a phase left half-done.

_RULING = (
    "Ben's ruling of 2026-08-03, recorded at §6 decision 5 of"
    " doc/PLAN-two-accents-on-one-chanted-word.md"
)


@dataclass(frozen=True)
class MamAllowance:
    marks: str
    sequence: str
    names: str
    verses: tuple[str, ...]
    note: str = ""


MAM_ALLOWANCES: tuple[MamAllowance, ...] = (
    MamAllowance(
        # Song of Songs 8:6 שַׁלְהֶ֥בֶתְיָֽה׃ -- a merkha on the open הֶ, and a U+05BD on the
        # stressed יָ immediately before sof pasuq, so that U+05BD is a silluq and not a meteg.
        # ``am.METEG`` is the codepoint's constant, named for the pair of readings it carries
        # (its underlying spelling is ``MTGOSLQ``); which of the two it is here is settled by the
        # sof pasuq that follows, and the scanner settles it the same way in emitting SILLUQ.
        marks=(
            am.LETTER * 3
            + am.MERKHA
            + am.LETTER * 3
            + am.METEG
            + am.LETTER
            + am.SOF_PASUQ
        ),
        sequence="merkha silluq",
        names=(
            "a secondary merkha in a silluq's chanted word, which neither Yeivin nor Breuer"
            " names; grammatical by Ben's ruling of 2026-08-03. The mam_allowances section of"
            " out/accgram/chanted-word-accents.json has the search behind that silence."
        ),
        verses=("ca8:6",),
        note=(
            "The silence is a measured one, not an assumed one: the §209 entry of"
            " YEIVIN_ENTRIES above carries the search, run on 2026-08-03 over the full ITM OCR"
            " and the CoS export, section by section. This is also the one atomic"
            " merkha-with-silluq chanted word in any of the three corpora, and all three have"
            " it with the same mark run, so the allowance rests on an accentuation a diplomatic"
            " transcription and a consensus text agree on rather than on a MAM-only one. MAM's"
            " four other chanted words with this token sequence are the שלף־חרב compounds ITM"
            " §357 accounts for, and the mark run is what keeps them out: each of them has a"
            " maqaf, and this key has none."
        ),
    ),
)


# --- the whitelist, derived from the tables above -----------------------------


def _build_named_token_sequences() -> dict[str, str]:
    out: dict[str, str] = {}
    for entry in YEIVIN_ENTRIES:
        for sequence in entry.sequences:
            if sequence in out:
                raise AssertionError(
                    f"two ITM sections claim the token sequence {sequence!r}:"
                    f" {out[sequence]} and {entry.section}"
                )
            out[sequence] = entry.section
    return out


# The whitelist, read straight off the inventory above so the two cannot part company: a token
# sequence, and the ITM section that names it.  Configuration-level, as decision 1 of the plan
# settled -- munax with revia is named wherever it stands, not only at §236's five places.  The
# closed lists stay where they are useful, as the survey's differential check against Yeivin;
# they are not consulted here, so nothing on a verdict path turns on a verse reference.
NAMED_TOKEN_SEQUENCES: dict[str, str] = _build_named_token_sequences()


def _build_allowance_index() -> dict[tuple[str, str], int]:
    """(mark run, token sequence) -> the index of the allowance it keys, checked for conflicts.

    Built here rather than beside ``MAM_ALLOWANCES`` so that the ITM check below has
    ``NAMED_TOKEN_SEQUENCES`` to run against: an allowance for a sequence Yeivin already names
    would be a ruling about a chanted word that needs none, and is a contradiction rather than a
    redundancy.
    """
    out: dict[tuple[str, str], int] = {}
    for index, entry in enumerate(MAM_ALLOWANCES):
        if entry.sequence in NAMED_TOKEN_SEQUENCES:
            raise AssertionError(
                f"the allowance for {entry.sequence!r} names a token sequence ITM"
                f" {NAMED_TOKEN_SEQUENCES[entry.sequence]} already names"
            )
        key = (entry.marks, entry.sequence)
        if key in out:
            raise AssertionError(
                f"two allowances claim one mark run with {entry.sequence!r}"
            )
        out[key] = index
    return out


# The second half of the whitelist, and the half that is Ben's rather than Yeivin's: a chanted
# word MAM has that no section of either book names, ruled grammatical for the time being.  Keyed
# on the mark run WITH the token sequence, so a per-verse allowance cannot spread to a chanted
# word that merely shares the pair -- MAM's four שלף־חרב compounds share ``merkha silluq`` with
# ca8:6 and match no key here.  ``scan_corpus`` reads it to pin each allowance against MAM, and
# ``classify_verse`` reads it to name a hit; nothing else does, ``mam_residue`` and
# ``wlc_chanted_word_residue_page`` both being closed against ``NAMED_TOKEN_SEQUENCES`` alone.
_ALLOWANCE_INDEX: dict[tuple[str, str], int] = _build_allowance_index()
