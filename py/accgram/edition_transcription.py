"""Compare a hand transcription of a printed edition's Decalogue against a vendored strand.

The pages in this family (``printed_decalogue_page`` and its Simanim / Koren satellites) place
real editions among the four IDEALIZED Wikisource strands.  Until now that placement rested on
SIGNAL WORDS -- a handful of accents that identify a strand -- which is enough to settle which
strand an edition follows but says nothing about whether it follows it in every accent.  This
module supports the stronger, accent-by-accent claim, by diffing a hand transcription of the
printed accents against the vendored ``in/accgram/printed_decalogue_teamim.json``.

A transcription is primary observation, read off the printed page (see
``in/accgram/edition_transcriptions/``).  It cannot be derived from anything in the repo, so it
is committed input, not generated output.  What this module adds is that the comparison becomes
mechanical and therefore repeatable: a re-vendoring or an upstream Wikisource revision that
moves an accent fails the test rather than silently invalidating prose on a page.

WHAT COUNTS AS ONE TOKEN (the conventions the transcriptions are written to):

* One token per ACCENT, which is normally one token per chanted word, a maqaf compound being
  one chanted word.  The exception is the compound that bears more than one accent -- its
  atoms each accented, which happens but is rare -- written ``mun-mer``, the dash standing for
  the maqaf itself, and contributing two tokens.  SimTiq's Exodus appendix Decalogue has two
  such compounds and they are its most interesting divergences, so this is not hypothetical.
  Contrast ``mun_leg``, where the underscore binds two marks into ONE accent.
* A postpositive or prepositive accent is written TWICE on a chanted word whose stress is not where
  the accent's fixed position puts it -- once at the fixed edge and once on the stressed
  syllable.  That is ONE accent.  ``_accent_tokens`` collapses an immediate repeat of the same
  accent within one chanted word; without this the Exodus elyon alone reports seven phantom
  differences.
* meteg (U+05BD) is dropped: it is not an accent.  Verse-finally the same codepoint is silluq,
  which IS an accent -- emitted, with sof pasuq, as the single token ``silsof``.
* Narrow-sense paseq is not an accent either.  Munax legarmeh is, but in the ACCENT TOKEN
  stream the two are folded together: a munax + U+05C0 is normalized to a plain munax on both
  sides (see ``_LEGARMEH_TOKENS``), so a legarmeh-vs-paseq difference is neither agreement nor
  disagreement THERE.  The kind is checked separately, off to the side of the token diff.  The
  wlc-utils#74 re-vendoring added ``faithful_chanted_verses`` to the source, which keeps the two
  Wikisource templates distinct where the folded ``chanted_verses`` collapses both to U+05C0;
  ``reference_pasoleg_kinds`` reads the reference kind of each stroke back out, so a
  transcription's own legarmeh/paseq claims can be checked against the strand's OWN reference
  rather than only against glyph shape and a cross-tradition nod to MAM-parsed-plus.

WHAT A DIFFERENCE MEANS.  Differences are not all of one weight, but they are all on one
scale, and maqaf is its bottom rung: a maqaf separates the ATOM it sits on from the next even
less than a conjunctive accent does.  So where the two texts put their maqafs differently, that
IS a difference in how the text is marked -- the mildest kind -- and it is counted ONCE, at the
atom whose marking changed, never as a regrouping plus a separate accent.  Both confirmed
differences in the Exodus elyon are of that kind, and so is one of the three in the Exodus
taxton.  Read a difference list alongside the atom it sits on to see which rung it is on: the
pages' verdicts are graded by that, not split into two ledgers.  (The trio briefly did keep two,
declaring a maqaf difference to be no accent difference at all; ``printed_decalogue_strands``'
``MAQAF_IS_THE_LAST_RUNG`` records why that was wrong.)

A maqaf USUALLY takes the place of a non-final atom's accent -- an atom standing as its own
chanted word must have one, while a non-final atom normally takes at most a meteg --
but usually is not always,
and the Exodus taxton is why the weaker word is the right one.  SimTiq has a munax on the
joined לא of לא־יהיה and of לא־תעשה, whose second atoms have merkha and qadma -- two accents on
one chanted word, where its own Wikisource strand, ws/ex/taxton/printed, has a meteg on the
joined לא and no accent.  (That one strand only: the eight do not agree at these sites -- the
four elyon strands have לא as a free chanted word with a munax, for one -- so read what another
strand has off the vendored data, not off this note.)  Those differences are two rungs up,
in the accents themselves, and an earlier version of this note asserted they could not occur.
Neither they nor the elyon's pair touch the disjunctive skeleton or the chanted verse
boundaries, which is the claim that has survived every transcription so far.

HOW RARE THAT IS IN PROSE, AND HOW ORDINARY IN POETRY (Ben, 2026-07-26; the Yeivin references
came from the FULL ITM OCR in ``../masorah-books/books/itm/md-export-of-docx``, which a first
pass missed by searching only the al-hatorah adaptation -- look in both).  That repo was
``yeivin-itm`` until 2026-07-31, when it was renamed and Breuer's CoS was merged into it.
Do not read a second accent on a prose compound as unremarkable.  Two different things put one
there, and they license different lists:

* **A SECONDARY ACCENT the compound simply inherits.**  Ben's rule: what turns up on a non-final
  atom is what can be the FIRST OF TWO accents on an ATOMIC word, so the second accent is nothing
  but a consequence of the compound being a single chanted word.  Yeivin's inventory of exactly
  that, under his own term "secondary accent", is short and prose-specific: munax-zaqef (ITM §221,
  frequent enough to count as a fourth variant of the zaqef melody), methiga-zaqef (§224 --
  metigah being in effect a special name for qadma used this way, hence the ``METHIGAZAQEF``
  scanner token, whose middle span deliberately crosses a maqaf), and the rare merkha and mahapakh
  on the word of a tevir (§§233, 241, about five cases apiece).  Ben's rule and Yeivin's list
  agree, which is the useful part; the list is a little longer than "metigah and a few munax".
  (ITM romanizes several of these differently from this repo, so grep the OCR for ITS spellings,
  not ours -- the same trap as Breuer's "hyphen" below.)
* **A MAQAF WRITTEN AFTER A WORD THAT KEEPS ITS OWN CONJUNCTIVE**, which is a manuscript habit and
  not a grammatical category at all.  Yeivin §293: "In a number of MSS, maqqef is occasionally
  marked after a word with a conjunctive accent.  This is most common where the word has
  penultimate stress ... possibly intended to show that the last syllable of the word has no
  accent."  §21 lists it among the features that TELL manuscripts apart, and L -- WLC's own base
  -- is named for doing it: L "marks maqqef after words with conjunctive accents, as ועזר־מצריו
  (Dt 33:7), showing, in this respect, a tradition somewhat different from the standard".  (§357
  is the neighbouring case, a maqaf after a word bearing a ga'ya that follows the accent.)  So an
  accent on a non-final atom in prose is neither unheard-of nor evenly distributed, and WHOSE
  habit it is is part of any question about one.

Two things Yeivin settles for the framing itself, worth not re-deriving.  §291: a maqaf "has no
musical motif of its own, and is therefore not considered an 'accent', either conjunctive or
disjunctive" -- the narrow sense the one-scale reading already concedes.  §292: a maqaf "could be
considered a superfluous sign, since it indicates the absence of any (other) accent sign.  In the
best MSS, however, maqqef is consistently marked after every word which does not have its own
accent" -- so the "atom left blank" GLOSS is Yeivin's own and holds as a near-rule for the best
manuscripts.  It is still not a definition, which is the distinction to keep.

The POETIC system is far more willing to put two accents on one chanted word, and that is
a dramatic difference between the two systems rather than a detail.  Breuer's Chapter 9 gives it
whole sections -- §§20-21 on a mafsik plus a servant, and on two servants, in one word; §§23-26
on the secondary mahapakh/merkha, which is the span he cites for it himself, twice, in §27 --
and §22 states the rule that governs them: two marks "appear in one word -- in the same manner
in which they are used to appear in two separate words".  He adds that the maqaf after a
secondary merkha is usually OMITTED, so the compound is written as two atoms although it is
chanted as one, with "but a few cases" where it survives.  §37 gathers THREE of those and calls
them all merkha marks: Job 6:10 ותהי־עוד and Prov 25:20 מעדה־בגד from the end of §27, and
Ps 78:7 מעללי־אל from §36's examples II.

The three do not behave alike in the corpora, which is the useful part.  In Job 6:10 and Prov
25:20 WLC has no maqaf: ותהי and עוד stand as two chanted words, and so do מעדה and בגד, where
MAM has each pair as one chanted word.  Ps 78:7 is the other way about -- WLC and MAM both have
מעללי־אל, and what differs there is the accent, MAM having a merkha on מעללי where WLC has a
meteg.  So no maqaf count can measure the poetic side: the asymmetry is real, but it lives in
Breuer's argument that an unhyphenated word still COUNTS as hyphenated, not in anything a scan
can see.  So SimTiq's two munax-on-לא are worth the attention this note gives them, and Koren's
``mun-mun`` on לא־תעשה more still.

CoS is greppable now, so CHECK a Breuer claim rather than restating one from here.  Chapter 9 is
``../masorah-books/books/cos/md-export-of-docx/C09-*.md`` -- the two books share one repo since
2026-07-31, so ITM above and CoS here are one clone apart, not two.  That repo's
``py/cos/check_cos_claims.py`` is
the differential check that caught the two errors this paragraph used to carry -- a §§22-26 that
was §22 plus §§23-26, and two surviving cases that were three.  It raises if a re-conversion
loses the evidence it pins.  Breuer's English mostly says "hyphen": "maqqef" and "maqaf" return
ZERO from a chapter that covers the subject at length, and that is the trap the ITM note above
compares itself to -- but a third spelling, "makaf", is the translator's and DOES occur, 27
times across nine files (2026-07-31), so grep "hyphen", "makaf" and מקף rather than two of them.

HOW OFTEN IT ACTUALLY HAPPENS is measured, not asserted, and the measurement is NOT here.  The
Tanakh-wide survey lives in ``maqaf_nonfinal_accents`` (+ ``_page``), which writes
``out/accgram/maqaf-nonfinal-accents.json`` and
``gh-pages/accgram/maqaf-nonfinal-accents.html`` from one run, and is where this note's claims
about rarity get their numbers.  Deliberately NO counts here: a number restated in a second file
is a number nothing keeps in step, which is the whole reason the survey was moved out of this
docstring.  What the page settles, qualitatively, is that an accent on a non-final atom happens in
well under one percent of prose maqaf compounds; that those cases split into Yeivin's grammatical
secondary accents and §293's bare scribal habit, most of them the former; and that Koren's
``mun-mun`` is NOT unprecedented -- 2 Chr 1:11 ויאמר־אלהים ׀ לשלמה is the same shape doing the
same job before a pazer -- but that its precedent is a MANUSCRIPT one, no printed edition being
known to have done it, SimTiq's munax on the joined לא being the nearest printed thing there is.
Read the page before restating any of that: it carries the corpus caveats that bound every one of
those findings, and the survey module's docstring carries the method.

WHAT THE TOKEN STREAM CANNOT SEE.  One token per ACCENT means a maqaf leaves no token of its
own, so a maqaf difference registers only through the accent count it changes.  Where an
edition joins two atoms and accents BOTH of them in the resulting compound -- ``koren_dt_elyon``'s
mun-mun on לא־תעשה -- the two sides emit identical tokens and the diff sees nothing.  Such a
difference is recorded by hand in the transcription's ``.txt`` and stated in the page's verdict
cell.  Making maqaf a token of its own would close the gap; that is issue wlc-utils#75, left undone here
because it touches every transcription and the reference derivation alike.

That claim is true and NOT the whole story, which is why ``transcription_parse`` exists
(issue wlc-utils#52).  An intact skeleton is a token-identity fact and says nothing about whether the
resulting sequence parses: the munax on the joined לא of לא־תעשה makes three servi before the
pashta where the grammar takes two, so that chanted verse is ungrammatical under the prose
checker even though every one of the page's divergences is conjunctive.
"""

from __future__ import annotations

import dataclasses
import difflib
import re
from pathlib import Path

import wlc_paths

PASEQ = "\N{HEBREW PUNCTUATION PASEQ}"
SOF_PASUQ = "\N{HEBREW PUNCTUATION SOF PASUQ}"
MTGOSLQ = "\N{HEBREW POINT METEG}"  # meteg, or silluq when verse-final
MAQAF = "\N{HEBREW PUNCTUATION MAQAF}"

# The three joiners, and the distinctions they draw.  ``-`` is a maqaf, binding two ACCENTS
# into one chanted word: ``mun-mer`` is a compound whose atoms are separately accented, rare
# but real, and it contributes two tokens because the reference side emits one per accent.
# ``_`` binds two MARKS into one accent: ``mun_leg`` is munax legarmeh, conceptually a single
# accent that merely happens to be written with a munax and a pasoleg, and it
# contributes one token.  Tight binding reads as tighter than a maqaf, which is the point.
#
# ``+`` is the SIMPLE-word counterpart of ``-``: two accents on one chanted word that is not a
# maqaf compound at all.  ``qad+ger`` is the case in hand -- qadma and geresh on a single atom,
# where the qadma is by convention called *metigah* rather than qadma (the same renaming
# applies in the compound case).  Like a maqaf compound it contributes one token per accent,
# because the reference side emits one per accent either way; unlike one, there is no maqaf,
# and collapsing the two notations would lose exactly the maqaf that every difference here has
# to be read against.
MAQAF_JOINER = "-"
UNIT_JOINER = "_"
SIMPLE_JOINER = "+"

# The two languages a chunk can be written in, and how each spells the joiners that split it
# into one token per accent.  UNIT_JOINER is in neither, which is what keeps ``mun_leg`` whole.
#
# The .txt writes a maqaf compound with MAQAF_JOINER; the line editor records the literal
# maqaf that was typed.  Otherwise the two agree, and both map onto the .txt's spelling, so
# one splitter serves both -- ``split_on_joiners`` below is the single place that knows a
# chunk can hold more than one accent.  It used to be three places, and when SIMPLE_JOINER
# was added to two of them the third went on rejecting ``qad+ger`` as an unknown abbreviation.
WRITTEN_ACCENT_JOINERS = {MAQAF_JOINER: MAQAF_JOINER, SIMPLE_JOINER: SIMPLE_JOINER}
EDITOR_ACCENT_JOINERS = {MAQAF: MAQAF_JOINER, SIMPLE_JOINER: SIMPLE_JOINER}

# Accent codepoint -> the shorthand the transcriptions use.
ACCENT_ABBREV = {
    "\N{HEBREW ACCENT ETNAHTA}": "etn",
    "\N{HEBREW ACCENT SEGOL}": "seg",  # segolta
    "\N{HEBREW ACCENT ZAQEF QATAN}": "zaq",
    "\N{HEBREW ACCENT ZAQEF GADOL}": "zaqg",
    "\N{HEBREW ACCENT TIPEHA}": "tip",
    "\N{HEBREW ACCENT REVIA}": "rev",
    "\N{HEBREW ACCENT ZARQA}": "zar",  # U+0598
    "\N{HEBREW ACCENT ZINOR}": "zar",  # U+05AE, the same accent as encoded in this data
    "\N{HEBREW ACCENT PASHTA}": "pash",
    "\N{HEBREW ACCENT YETIV}": "yet",
    "\N{HEBREW ACCENT TEVIR}": "tev",
    "\N{HEBREW ACCENT GERESH}": "ger",
    "\N{HEBREW ACCENT GERESH MUQDAM}": "germ",
    "\N{HEBREW ACCENT GERSHAYIM}": "ger2",
    "\N{HEBREW ACCENT TELISHA GEDOLA}": "tg",
    "\N{HEBREW ACCENT PAZER}": "paz",
    "\N{HEBREW ACCENT MUNAH}": "mun",
    "\N{HEBREW ACCENT MAHAPAKH}": "mah",
    "\N{HEBREW ACCENT MERKHA}": "mer",
    "\N{HEBREW ACCENT MERKHA KEFULA}": "mer2",
    "\N{HEBREW ACCENT DARGA}": "dar",
    "\N{HEBREW ACCENT QADMA}": "qad",
    "\N{HEBREW ACCENT TELISHA QETANA}": "tq",
}

# Spellings a transcriber may reasonably write, normalized onto the shorthand above.
ALIASES = {
    "pashta": "pash",
    "zaqef": "zaq",
    "zarq": "zar",
    "gershayim": "ger2",
    "munax": "mun",  # transcriptions are plain ASCII, so x for the letter xet
    "munaḥ": "mun",
}

# Legarmeh is set aside for now (see the module docstring): both sides collapse to a plain
# munax so that a PASOLEG position is scored as neither agreement nor disagreement.
_LEGARMEH_TOKENS = ("mun_leg", "mun_PASOLEG")

# What is typed into the line editor (transcription_editor.py), onto the Latin shorthand the
# .txt is written in.  Transcribing from a Hebrew page in Latin means translating every mark
# in your head while also holding your place on the line, so the editor takes Hebrew and the
# mapping happens here instead.
#
# The rule is ANY UNIQUE PREFIX of the accent's Hebrew name: זר is zarqa, פז is pazer, סג is
# segolta, and the full name always works.  So there is no code to memorize, and no need to
# agree a spelling in advance for an accent a page has not yet produced -- which the earlier
# fixed table did require, and which was the reason six accents were deliberately missing
# from it.  A prefix matching more than one name is an error naming the candidates, not a
# guess: adding zaqef gadol later turns a bare זק from unambiguous into rejected, which is
# the safe direction.
#
# Bare זקף is zaqef QATAN by name, not by convention -- the unqualified accent's name simply
# is זקף, so an exact match wins over any longer name that extends it.  The same rule keeps
# מרכא off מרכא כפולה and גרש off גרשיים.
HEBREW_NAMES = {
    "אתנחתא": "etn",
    "סגולתא": "seg",
    "זקף": "zaq",
    "טפחא": "tip",
    "רביע": "rev",
    "זרקא": "zar",
    "פשטא": "pash",
    "יתיב": "yet",
    "תביר": "tev",
    "גרש": "ger",
    "גרשיים": "ger2",
    "תלישא גדולה": "tg",
    "פזר": "paz",
    "מונח": "mun",
    "מהפך": "mah",
    "מרכא": "mer",
    "דרגא": "dar",
    "קדמא": "qad",
    "תלישא קטנה": "tq",
    "סילוק": "silsof",
}

# Spellings the prefix rule cannot reach, and that the Exodus taxton was already transcribed
# in.  תג/תק take a letter from each word of a two-word name, which is not a prefix of it at
# all; גר prefixes גרש and גרשיים alike, so it would be rejected as ambiguous even though
# geresh is the unmarked member of that pair and is what גר has always meant here.
HEBREW_SHORTHAND = {
    "תג": "tg",
    "תק": "tq",
    "גר": "ger",
}

# Written after UNIT_JOINER, binding a second mark into the accent named before it.  Kept
# apart from the accent names so that a bare לג cannot resolve to a token on its own.
HEBREW_MODIFIERS = {
    "לגרמיה": "leg",
}

# The bracketed asides a transcription may carry, each mapped onto the way the .txt spells it
# and the pasoleg KIND it records.  An aside is not an accent and is dropped from both token
# streams; what it adds is the one fact the vendored data cannot hold, since that fetch folds
# {{מ:לגרמיה}} and {{מ:פסק}} alike onto U+05C0 -- WHICH kind of stroke stands there.
#
# Three kinds, not two, because an edition may not draw the distinction at all.  Koren has
# the stroke without saying which it is, so writing either מונ_לג (asserting legarmeh) or
# [פסק] (asserting narrow-sense paseq) would claim something the book does not; [פסלג] says
# "a pasoleg stands here, kind unspecified".  The name is the repo's existing portmanteau for
# exactly this ambiguity -- PASOLEG in mb_cmn/hebrew_punctuation.py.
#
# Both spellings of each aside are keys, because the two serializations differ: the editor
# takes Hebrew and the .txt is written in ASCII, and an overclaim can re-enter through either.
PASOLEG_ASIDES = {
    "[פסק]": ("[paseq]", "paseq"),
    "[paseq]": ("[paseq]", "paseq"),
    "[פסלג]": ("[pasoleg]", "unspecified"),
    "[pasoleg]": ("[pasoleg]", "unspecified"),
}

# Notation that asserts a pasoleg's kind, in either serialization and either spelling.  An
# edition whose header says it does not distinguish the two must contain none of these.
KIND_ASSERTING = ("mun_leg", "מונ_לג", "[פסק]", "[paseq]")


def _resolve_name(
    written: str, names: dict[str, str], shorthand: dict[str, str]
) -> str:
    """One thing typed into the editor -> its Latin shorthand, by exact name or unique prefix.

    Exact matches -- a name, or an agreed shorthand -- are taken before any prefix search, so
    that a name which merely extends another (גרשיים over גרש, זקף גדול over זקף) cannot make
    the shorter one ambiguous.
    """
    if written in shorthand:
        return shorthand[written]
    if written in names:
        return names[written]
    matches = sorted(name for name in names if name.startswith(written))
    if not matches:
        raise ValueError(f"unknown Hebrew accent abbreviation {written!r}")
    if len(matches) > 1:
        raise ValueError(f"ambiguous Hebrew accent abbreviation {written!r}: {matches}")
    return names[matches[0]]


def hebrew_token(written: str) -> str:
    """One thing typed into the editor -> the Latin shorthand, ``mun_leg`` included."""
    head, joiner, tail = written.partition(UNIT_JOINER)
    accent = _resolve_name(head, HEBREW_NAMES, HEBREW_SHORTHAND)
    if not joiner:
        return accent
    return accent + UNIT_JOINER + _resolve_name(tail, HEBREW_MODIFIERS, {})


def _aside(written: str) -> tuple[str, str]:
    """One bracketed aside -> ``(the .txt's spelling of it, the pasoleg kind it records)``.

    Unknown asides RAISE rather than falling back to a kind.  The fallback used to be
    "paseq", which turned any aside nobody had taught this vocabulary into a silent claim
    that a narrow-sense paseq stands there -- the strongest of the three kinds, asserted by
    accident.  Positional asides such as ``[page break]`` live only in .txt bodies today, and
    if one ever reaches an export -- plausible once Koren's two-page Deuteronomy is typed --
    raising forces the vocabulary to be extended deliberately.
    """
    try:
        return PASOLEG_ASIDES[written]
    except KeyError:
        raise ValueError(
            f"unknown transcription aside {written!r}:"
            f" expected one of {sorted(PASOLEG_ASIDES)}"
        ) from None


def aside_kind(written: str) -> str:
    """The pasoleg kind a bracketed aside records: paseq, or unspecified."""
    return _aside(written)[1]


UNCERTAIN_FIELDS = ("word", "reading", "why")


def uncertain_readings(pages: list[dict]) -> list[dict]:
    """Every reading the transcriber flagged as not fully read off the page.

    A transcription's authority is that it is primary observation, so a token supplied partly
    from context or expectation -- because the scan is blotched, or the printing is -- is a
    hole in exactly that claim.  It is also the hole the review loop can never find: a reading
    taken from expectation matches the reference BY CONSTRUCTION, so it lands in the agreeing
    majority the loop never inspects, and a "no divergences" result silently absorbs it.
    Hence recorded per line in the export, reported by ``transcription_check``, and counted in
    the .txt header, where a test holds the count to what the export actually carries.

    Each entry names the ``word``, the ``reading`` taken, and ``why`` it is uncertain; the page
    and line come from where it sits.  Resolving one means going back to the printed page --
    the physical book, if the scan is what is at fault -- and either confirming the reading or
    correcting it, then dropping the entry.
    """
    out: list[dict] = []
    for page in pages:
        label = page.get("stem", "?").split("_")[-1]
        for line in page["lines"]:
            for entry in line.get("uncertain", []):
                missing = [f for f in UNCERTAIN_FIELDS if not entry.get(f)]
                if missing:
                    raise ValueError(
                        f"{label} line {line['n']}: uncertain entry missing {missing}"
                    )
                out.append({**entry, "page": label, "line": line["n"]})
    return out


def is_header_field(stripped: str) -> bool:
    """True when a stripped .txt line is a ``key: value`` header field, not a body line.

    Shared with ``transcription_build``, which splits a committed .txt into the header it
    preserves and the body it rewrites.  That split has to agree with what this module treats
    as a field: a line the two classified differently would be preserved as header AND
    regenerated as body, so it would be committed twice.  ``[paseq]`` is excluded because a
    bracketed aside is a body chunk however it is spelled, and a field name with a space in it
    is not a field -- a body line could otherwise open a header by accident.
    """
    if ":" not in stripped or stripped.startswith("["):
        return False
    return " " not in stripped.partition(":")[0].strip()


def transcriptions_dir() -> Path:
    """Committed hand transcriptions, one file per edition-Decalogue.

    Filenames are ``<edition>_<book>_<reading>``: the same Decalogue exists in more than one
    edition, so the edition has to be in the stem for the stems to stay distinct.
    """
    return wlc_paths.in_dir() / "accgram" / "edition_transcriptions"


def strand_name(key: tuple[str, str, str]) -> str:
    """One vendored strand's display name: ``ws/ex/taxton/printed``.

    The ``(book, reading, tradition)`` triple alone was only sort of clear from context.  The
    ``ws/`` prefix says outright that the strand is one of the eight IDEALIZED Wikisource
    strands vendored in ``in/accgram/printed_decalogue_teamim.json``, and it earns its keep
    most on the manuscript triples, where ``ws/dt/elyon/manuscript`` reads plainly as a
    Wikisource-vendored idealization OF the manuscript tradition rather than as a manuscript.

    DISPLAY ONLY.  The data keys -- the triple itself, and the ``book``/``reading``/
    ``tradition`` fields in the vendored JSON -- keep the bare form.  CTR is a separately
    vendored strand (issue wlc-utils#73) and is never named this way.
    """
    return "/".join(("ws",) + tuple(key))


@dataclasses.dataclass(frozen=True)
class Transcription:
    """One hand-transcribed Decalogue: its header fields, accent tokens, and body chunks.

    ``tokens`` is the ACCENT stream the comparison runs on: legarmeh folded onto a plain
    munax, asides dropped, one entry per accent.  ``chunks`` is the body as written, one
    entry per whitespace-separated piece and asides KEPT -- so a multi-accent word is still
    one chunk and a ``[paseq]`` still stands where it was read.  ``transcription_parse``
    needs both facts to build a scanner mark body: the stroke is a mark the scanner reads
    (it decides legarmeh from a munax + stroke before a revia), and a maqaf compound has to
    stay one chanted word.
    """

    path: Path
    header: dict[str, str]
    tokens: tuple[str, ...]
    chunks: tuple[str, ...]

    @property
    def key(self) -> tuple[str, str, str]:
        """The ``(book, reading, tradition)`` triple naming the strand to compare against."""
        return (self.header["book"], self.header["reading"], self.header["tradition"])

    @property
    def label(self) -> str:
        edition = self.header.get("edition", "?")
        pages = self.header.get("pages", "?")
        return f"{edition} {strand_name(self.key)} (pp. {pages})"


@dataclasses.dataclass(frozen=True)
class Difference:
    """One region where transcription and reference disagree.

    ``word`` is the reference word the region starts on -- the thing to look at to see which
    rung of the scale the difference is on, an accent or the maqaf below them.
    """

    kind: str  # difflib opcode: "replace", "delete", "insert"
    ref_index: int
    reference: tuple[str, ...]
    transcribed: tuple[str, ...]
    word: str

    def describe(self) -> str:
        ref = " ".join(self.reference) or "(nothing)"
        got = " ".join(self.transcribed) or "(nothing)"
        return f"at token {self.ref_index} ({self.word}): reference {ref} / transcribed {got}"


def normalize_token(token: str) -> str:
    """One written token as the comparison scores it: aliases resolved, legarmeh folded.

    Folding legarmeh onto a plain munax belongs to the COMPARISON, not to a transcription
    (see ``hebrew_chunks``): both sides of the diff pass through here, and only here.
    """
    token = ALIASES.get(token, token)
    return "mun" if token in _LEGARMEH_TOKENS else token


def split_on_joiners(chunk: str, joiners: dict[str, str]) -> list[tuple[str, str]]:
    """Split a chunk into ``(part, the WRITTEN joiner before it)``, in order.

    The first part's joiner is ``""``.  ``joiners`` maps each joiner as the chunk spells it
    onto the way the .txt spells it, so a caller that only wants the parts can drop the second
    element and one that has to rebuild the .txt spelling has it to hand.
    """
    out: list[tuple[str, str]] = []
    part = ""
    joiner = ""
    for ch in chunk:
        if ch in joiners:
            out.append((part, joiner))
            part, joiner = "", joiners[ch]
        else:
            part += ch
    out.append((part, joiner))
    return out


def written_accents(chunk: str) -> list[str]:
    """One chunk as the .txt writes it -> its per-accent parts."""
    return [part for part, _ in split_on_joiners(chunk, WRITTEN_ACCENT_JOINERS)]


def editor_accents(chunk: str) -> list[tuple[str, str]]:
    """One chunk as the line editor records it -> ``(Hebrew accent, .txt joiner before it)``.

    The one place that knows how an editor chunk holding more than one accent comes apart.
    ``transcription_check`` needs the parts alone, to resolve each with its own printed-line
    origin and to count how many tokens a chunk contributes; ``_hebrew_chunk`` needs the
    joiners too, to write the .txt.  Both take them from here.
    """
    return split_on_joiners(chunk, EDITOR_ACCENT_JOINERS)


def expand_chunk(chunk: str) -> list[str]:
    """One written chunk -> the token(s) it stands for.

    Almost always one.  A chanted word bearing more than one accent is the exception -- a maqaf
    compound (``mun-mer``) or a simple word (``qad+ger``) -- and it contributes one token per
    accent either way.  Splitting on the ACCENT joiners alone is what makes ``mun_leg`` stay
    whole here.
    """
    return [normalize_token(part) for part in written_accents(chunk)]


def rejoin_editor_chunks(items: list[tuple[str, object]]) -> list[tuple[str, object]]:
    """Rejoin maqaf compounds the editor's line breaks split, asides kept in place.

    ``items`` are ``(written, payload)`` pairs in reading order -- the payload is whatever the
    caller needs carried along, a printed-line origin or nothing at all.  The editor records a
    multi-accent maqaf compound with a literal maqaf between its accents; when such a compound
    straddles a printed line break its accents arrive on two different lines, so a chunk left
    ending in a maqaf takes the following chunk with it, and keeps the payload of the piece it
    STARTED on -- that is the line to go back and re-read.

    A bracketed aside carries no accent, so it passes through untouched and never takes part
    in the rejoining: a compound continues across an intervening aside.  This is the ONE
    implementation of the rejoin -- ``hebrew_chunks`` here and ``transcription_check`` both
    call it, after the two drifted apart on exactly the aside case while each had its own.
    """
    out: list[tuple[str, object]] = []
    last_real = -1  # index into ``out`` of the last non-aside chunk
    for written, payload in items:
        if written.startswith("["):
            out.append((written, payload))
        elif last_real >= 0 and out[last_real][0].endswith(MAQAF):
            joined, kept = out[last_real]
            out[last_real] = (joined + written, kept)
        else:
            out.append((written, payload))
            last_real = len(out) - 1
    return out


def hebrew_chunks(lines: list[str]) -> list[str]:
    """Latin shorthand for the Hebrew abbreviations typed into the line editor.

    ``lines`` are the editor's per-line strings, in page order.  Returns one chunk per chanted
    word, written the way the .txt writes it: a multi-accent maqaf compound keeps its dash and
    ``mun_leg`` keeps its underscore.  Normalization -- folding legarmeh onto a plain munax --
    is deliberately NOT done here.  It belongs to the comparison, not to the transcription,
    and doing it here would make the .txt this produces claim less than what was observed.

    ``rejoin_editor_chunks`` undoes the editor's line breaks first; the asides it keeps in
    place are dropped here, exactly as ``load_transcription`` drops them from the .txt.
    ``[פסק]`` and ``[פסלג]`` (see ``PASOLEG_ASIDES``) are worth recording on the page they
    were read from, but neither is an accent and so neither is a token on either side of the
    comparison.  ``txt_lines`` is the derivation that keeps them.
    """
    items = [(chunk, None) for line in lines for chunk in line.split()]
    return [
        _hebrew_chunk(written)
        for written, _ in rejoin_editor_chunks(items)
        if not written.startswith("[")
    ]


def txt_lines(lines: list[str]) -> list[str]:
    """The editor's per-line strings -> the .txt body, ONE .txt line per printed line.

    The .txt a transcription is committed as is DERIVED from the corrected export rather than
    typed a second time, so the two cannot drift; this is that derivation.  It differs from
    ``hebrew_chunks`` in two ways, both of them about being a body rather than a token stream:
    the printed line structure is kept, so a token can still be checked against the line it
    was read off, and asides are kept too, spelled the way the .txt spells them.

    Keeping the aside is the point of having one.  It is dropped from both token streams --
    it is not an accent -- so the .txt body is the only place a reader of the committed file
    can see that a stroke stood there and which kind it was; simtiq_dt_elyon.txt shows its
    ``[paseq]`` inline for exactly that reason.  A rejoined maqaf compound lands on the line
    it STARTED on, matching what ``rejoin_editor_chunks`` carries.
    """
    items = [(chunk, i) for i, line in enumerate(lines) for chunk in line.split()]
    out: list[list[str]] = [[] for _ in lines]
    for written, i in rejoin_editor_chunks(items):
        out[i].append(
            _aside(written)[0] if written.startswith("[") else _hebrew_chunk(written)
        )
    return [" ".join(parts) for parts in out]


def _hebrew_chunk(chunk: str) -> str:
    """One editor chunk -> the way the .txt writes it, both accent joiners preserved.

    The editor records a maqaf compound with a literal maqaf between its accents, and a
    multi-accent simple word with the ``+`` that is typed.  ``editor_accents`` maps each onto
    its own written joiner, so the .txt keeps saying which of the two was seen on the page.
    """
    return "".join(
        joiner + hebrew_token(accent) for accent, joiner in editor_accents(chunk)
    )


def _accent_tokens(verses: list[str]) -> tuple[list[str], list[str], list[str]]:
    """(tokens, words, pasoleg_words) for a vendored strand's chanted verses.

    ``words[k]`` is the chanted word token ``k`` sits on, so a caller can see whether a
    difference is at the maqaf rather than in an accent.
    """
    tokens: list[str] = []
    words: list[str] = []
    pasoleg: list[str] = []
    for verse in verses:
        verse_words = verse.split()
        for word in verse_words:
            previous = None
            for i, ch in enumerate(word):
                abbrev = ACCENT_ABBREV.get(ch)
                if abbrev is None:
                    continue
                if abbrev == previous:
                    continue  # doubled postpositive/prepositive: one accent, one token
                previous = abbrev
                if abbrev == "mun" and word[i + 1 :].endswith(PASEQ):
                    pasoleg.append(word)
                tokens.append(abbrev)
                words.append(word)
        if verse.rstrip().endswith(SOF_PASUQ):
            tokens.append("silsof")
            words.append(verse_words[-1] if verse_words else "")
    return tokens, words, pasoleg


def _version_of(source: dict, key: tuple[str, str, str]) -> dict:
    book, reading, tradition = key
    return next(
        v
        for v in source["versions"]
        if v["book"] == book and v["reading"] == reading and v["tradition"] == tradition
    )


def reference_tokens(source: dict, key: tuple[str, str, str]):
    """The reference accent tokens for one ``(book, reading, tradition)`` strand."""
    return _accent_tokens(_version_of(source, key)["chanted_verses"])


def _faithful_pasoleg_kinds(faithful_verse: str) -> list[str]:
    """The stroke kinds in one faithful (unfolded) verse, in reading order.

    ``legarmeh`` for ``{{מ:לגרמיה}}`` and ``paseq`` for ``{{מ:פסק}}`` -- the two Wikisource
    templates that the folded ``chanted_verses`` collapses to an indistinguishable U+05C0.
    """
    return [
        "legarmeh" if m.group(1) == "לגרמיה" else "paseq"
        for m in re.finditer(r"\{\{מ:(לגרמיה|פסק)\}\}", faithful_verse)
    ]


def reference_pasoleg_kinds(source: dict, key: tuple[str, str, str]) -> list[str]:
    """The kind of each U+05C0 stroke in a strand's reference, in reading order.

    ``legarmeh`` or ``paseq``, read from the version's ``faithful_chanted_verses`` -- the
    distinction the folded ``chanted_verses`` cannot express, vendored by the wlc-utils#74 re-vendor.
    Aligned with the reference pasoleg positions ``_accent_tokens`` finds in the folded text:
    the k-th kind is the k-th pasoleg in reading order, which is what lets ``transcription_check``
    map a transcribed stroke to a reference kind.  A count mismatch means the faithful and
    folded forms have drifted, so it raises rather than return a silently misaligned list.
    """
    version = _version_of(source, key)
    faithful = version.get("faithful_chanted_verses")
    if faithful is None:
        raise ValueError(
            f"{strand_name(key)}: vendored source has no faithful_chanted_verses -- re-vendor "
            "via printed_decalogue_fetch.py (issue wlc-utils#74)"
        )
    kinds = [kind for fv in faithful for kind in _faithful_pasoleg_kinds(fv)]
    _, _, pasoleg = _accent_tokens(version["chanted_verses"])
    if len(kinds) != len(pasoleg):
        raise ValueError(
            f"{strand_name(key)}: {len(kinds)} faithful strokes but {len(pasoleg)} folded "
            "pasoleg positions -- the faithful and folded forms disagree"
        )
    return kinds


def load_transcription(path: Path) -> Transcription:
    """Parse a transcription file: ``#`` comments, ``key: value`` header, then tokens."""
    header: dict[str, str] = {}
    tokens: list[str] = []
    chunks: list[str] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if is_header_field(stripped):
            field, _, value = stripped.partition(":")
            header[field.strip()] = value.strip()
            continue
        for chunk in re.findall(r"\[[^\]]*\]|\S+", stripped):
            chunks.append(chunk)
            if chunk.startswith("["):
                continue  # a bracketed aside such as "[page break]" carries no accent
            tokens.extend(expand_chunk(chunk))
    missing = {"book", "reading", "tradition"} - set(header)
    if missing:
        raise ValueError(f"{path}: transcription header missing {sorted(missing)}")
    return Transcription(
        path=path, header=header, tokens=tuple(tokens), chunks=tuple(chunks)
    )


def load_all_transcriptions() -> list[Transcription]:
    """Every committed transcription, sorted by filename."""
    return [load_transcription(p) for p in sorted(transcriptions_dir().glob("*.txt"))]


def compare(source: dict, transcription: Transcription) -> list[Difference]:
    """Every region where ``transcription`` disagrees with its vendored strand."""
    ref, words, _ = reference_tokens(source, transcription.key)
    got = [normalize_token(t) for t in transcription.tokens]
    matcher = difflib.SequenceMatcher(a=ref, b=got, autojunk=False)
    out: list[Difference] = []
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == "equal":
            continue
        out.append(
            Difference(
                kind=tag,
                ref_index=i1,
                reference=tuple(ref[i1:i2]),
                transcribed=tuple(got[j1:j2]),
                word=words[min(i1, len(words) - 1)] if words else "",
            )
        )
    return out
