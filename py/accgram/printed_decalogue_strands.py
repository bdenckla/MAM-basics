r"""Shared computation for the two printed-Decalogue pages: the four cantillation strands
of the Exodus Decalogue's opening אנכי...מצותי span, resolved live from the vendored data.

This module is pure computation -- no HTML, no display/editorial vocabulary in its *return
values* -- so both companion pages can depend on it without either depending on the other:

  * ``printed_decalogue_page`` (issue wlc-utils#52) grammar-checks the printed vs manuscript Decalogue
    accentuations and now also lays out the four strands as a styled range table.
  * ``printed_decalogue_simanim_page`` (issue wlc-utils#62) documents Simanim's Tiqqun as an independent
    printed-tradition edition and links back to the four-strands table on the main page.

Each of the four Exodus readings (m-trad / p-trad x taḥton / elyon) is read from
``in/accgram/printed_decalogue_teamim.json`` (Hebrew Wikisource data): the leading chanted verses
covering the אנכי...מצותי span are pulled from the data, and the accents on אנכי, עבדים and
על־פני are derived from the marks, so the strands can never drift from the data.
``resolve_readings`` pins each derivation against ``READING_SPECS`` / ``STRUCTURE`` and raises
``AssertionError`` on any divergence -- this build-fails-on-data-drift behavior fires at page-1
generation and in the tests, and must never be softened to a warning.  ``resolve_pausal`` and
``check_tirtsax`` do the same for the appendix's vowels: the pausal alternation at על־פני and מתחת,
and the vocalization of תרצח in all eight readings.

Editorial / style conventions for the rendered prose (agreed with Ben; keep them when editing
any page they govern).  This list is the repo's home for them -- ``CLAUDE.md`` points here.

SCOPE.  The bullets divide into two kinds, and the difference matters when a rule is invoked
somewhere else.  TRIO-ONLY: the strand names in Hebrew letters, "signal word", the maqaf scale,
the scoped "no difference anywhere", the ``ROM_*`` single-sourcing and its italic wrapping, the
two Simanim editions and their determiner, and the attribute exemption -- all of these are about
the printed-Decalogue pages' own subject matter.  REPO-WIDE, and applied to every accgram page:
atom vs chanted word, "cantillation" over "accentuation", the real em dash, and never opening an
English sentence with a Hebrew word.

* **The two chant-strands are named in Hebrew letters -- תחתון / עליון -- NEVER transliterated
  and NEVER translated.**  No "taḥton"/"elyon" and no "upper"/"lower" in the output: the
  upper/lower glosses invite confusion with above-letter vs below-letter accents, which is *not*
  what the names mean, and for a reader who doesn't know the terms no gloss beats a misleading
  one.  The full ``טעם תחתון`` / ``טעם עליון`` appears ONLY at first mention; everywhere after,
  drop the טעם -- bare עליון is read as "the [טעם] עליון".  The romanized "taḥton"/"elyon" survive
  only as *internal keys* (``READING_SPECS`` / ``STRUCTURE`` names) and inside ``title`` / ``alt``
  attributes; render via the ``TAHTON`` / ``ELYON`` string constants (or ``render_reading_name``).
  Verbatim quoted source Hebrew (e.g. ``בלא טעם עליון``) keeps whatever it says.  This is a
  cross-repo rule (cf. MAM-basics ``py/versification_and_cantillation/doc.py``).
* Prefer "**cantillation**" to "accentuation".
* **Never a loose "word": say "atom" or "chanted word" where one of them is meant** (issue wlc-utils#81).
  An ATOM is one written word, the thing a maqaf joins to the next; a CHANTED WORD is either a
  lone atom or a whole maqaf compound -- the unit cantillation operates on, normally bearing one
  accent.  Two of the Shabbat commandment's three signal words are compounds, and על־פני is one,
  so the trio's central claims are about chanted words and saying "word" leaves them uncheckable.
  Name a compound whole (על־פני, לא־תעשה), never a bare half of one.  ``MAQAF_IS_THE_LAST_RUNG``
  introduces "atom" to the reader with an appositive gloss, which is what licenses the bare term
  elsewhere on the pages.  Plain "word" survives only for an ordinary English word ("in other
  words", "a great many Hebrew words take one vowel where the reading pauses") and inside quoted
  or translated source material, which keeps whatever it says.
* **"Signal word" is the trio's ONE term for a chanted word whose accent tells strands apart** -- it
  replaced the older "milestone word", which said only "notable position" and not "this is where
  you look".  It now names TWO distinct sets, and the pages must never collapse them into one
  claim: (a) within the אנכי...מצותי span, עבדים and על־פני, whose accent PAIR uniquely identifies
  which of the four strands a text has (see ``resolve_readings``' pairwise-distinctness check);
  and (b) at the Deuteronomy Shabbat commandment, the trio of disjunctively accented chanted words that
  tells p-trad accents from m-trad ones (see ``SHABBAT_SIGNAL_SHORTHAND``).  Their jobs are
  complementary, not redundant -- the doctrine is spelled out at that constant.  אנכי and מצותי
  are the span's shared frame, NOT signal words: every strand starts at the one and ends a
  chanted verse at the other, so neither distinguishes anything.
* **ONE scale, with maqaf at the bottom of it -- there is no second ledger for maqaf
  differences.**  A verdict measures how far down that scale a Decalogue's agreement with its
  Wikisource strand reaches: chanted verse boundaries, then the disjunctive skeleton, then the
  conjunctives, then the maqafs.  A maqaf an edition adds or drops IS a difference in how the
  text is marked --
  the mildest one there is, since a maqaf separates its atom from the next even less than a
  conjunctive does -- and it is counted ONCE, at the atom whose marking changed, never as a
  regrouping plus an accent.  So a verdict cell names the first rung that breaks and what breaks
  it, and "every accent" is never said with a maqaf difference tucked underneath it.  The scale is
  stated to the reader verbatim on all three pages via ``MAQAF_IS_THE_LAST_RUNG``: splice that
  constant, don't paraphrase it.  Its guardrail comment records the convention this replaced (a
  2026-07-25 audit fix that made maqaf differences non-differences) and why that one was wrong.
* **Never write a bare "no difference anywhere" in a verdict cell; scope it, "no difference
  anywhere the comparison reaches".**  What backs these cells is a hand transcription of the
  printed ACCENTS, so "anywhere" can only ever mean "anywhere the comparison reaches", and an
  unscoped phrasing invites a reader to take it for the whole page.  Two things fall outside.  A
  maqaf, which the .txt line records but the token stream drops: ``koren_dt_elyon`` joins לא־תעשה
  where its Wikisource strand sets the two atoms apart, and since Koren accents BOTH atoms of the
  compound the two sides emit the same two tokens, so a zero-divergence result is not evidence of
  no difference.  (That blindness is a gap
  now that the scale above counts such a difference; making maqaf a token of its own is issue
  wlc-utils#75.)  And the POINTING: the two תחתון strands part at תרצח in a vowel and nothing
  else, qamats m-trad against patax p-trad on the same tipexa, which the diff cannot see in either
  book.  The scoped phrasing costs one word and is true; the bare one was already false once (the
  Koren Deuteronomy appendix row, 2026-07-25 claim audit finding 3).  Where a vowel or a maqaf HAS
  been checked off the page, say so in the cell and put the evidence in the transcription's
  ``.txt`` comment block -- that is a primary observation about the edition, not something the
  harness establishes, and no test will defend it.
* **Accent/mark romanizations are single-sourced as ``ROM_*`` constants** (pashta, tipeḥa,
  etnaḥta, revia, segolta, silluq, sof pasuq, meteg, maqaf, legarmeh, paseq, the two vowels of
  the pausal alternation, + a few compounds).
  They are shared by the ``_ACCENT_NAMES`` derivation table, the ``READING_SPECS``
  expected-accent pins, and the prose of all three pages -- so a printed name can't drift from
  the derived one.  Don't retype these spellings inline; ``tests/test_transliterations.py``
  guards them tree-wide.  (``_CP_*`` = the codepoint constants, distinct from the ``ROM_*`` word
  forms.)  They stay PLAIN ``str`` here on purpose: ``_accent_of`` returns them and
  ``READING_SPECS`` compares them, so they must never become HTML.
* **Every romanized accent/mark name renders italic, inside ``<span class="romanized">``**
  (``gh-pages/style.css``; matching the MAM-simple island, which italicizes every such term).
  The pages do the wrapping, not this module -- each aliases the ``ROM_*`` strings through
  ``py_html.my_html_span_romanized.rmn`` ONCE at module level, so every prose site is styled
  without a per-site call (settled as issue wlc-utils#65, finding C2).  This is why the wrapped aliases
  are HTML nodes, not strings, and so cannot be interpolated into an f-string -- splice them
  into a contents tuple instead.  Book/apparatus terms (Tiqqun, ḥumash, Keter, qere/ketiv,
  pisqa) are NOT accent names and stay unwrapped; so does the ``pashta_phrase`` code identifier,
  which is a checker error name rather than a transliteration.
* **A bare "Simanim" never names an edition.**  Feldheim publishes two that this trio reads --
  the *Simanim Tiqqun* (the tiqqun qorim; Decalogues on pp. 83-84, 208-209, 246, 247) and the
  *Simanim Tanakh* (pp. 119-120, 297-298, 350, 351) -- and they do not even agree: the Tiqqun is
  p-trad and the Tanakh m-trad.  The repo's vocabulary predates the second, so an unqualified
  "Simanim" reads as the Tiqqun by historical accident alone.  Write **SimTiq** / **SimTan**
  (lowercase ``simtiq`` / ``simtan`` in identifiers and transcription stems) in code, comments,
  docstrings, tests and docs; in RENDERED prose write the full "Simanim Tiqqun" / "Simanim
  Tanakh", or a bare "the Tiqqun" once the passage has named it, since the shorthand is repo
  jargon that a reader of a published page has not met.  Two things a bare "Simanim" may still
  do: name the *page* (``printed-decalogue-simanim.html`` documents BOTH editions, so "the
  Simanim page" is right), and name the publisher or both books at once ("the two Simanim
  editions", "no digital Simanim edition exists").
* **The edition name takes a determiner in running prose: "the Simanim Tiqqun" or "Simanim's
  Tiqqun", never a bare "Simanim Tiqqun prints ...".**  "Simanim" is the publisher, not part of
  a title, so it is doing a possessive's work; the bare noun-noun compound instead reads as a
  fixed brand name.  Contrast "Koren", which by metonymy IS the edition's name and so correctly
  takes no determiner ("Koren has X at Y" is fine, "Simanim Tiqqun has X at Y" is not).  Between
  the two forms, prefer the ARTICLE whenever a genitive follows -- "the Simanim Tiqqun's own
  stance", not the double-genitive "Simanim's Tiqqun's own stance" -- and the possessive when it
  parallels a neighbouring "Koren's Classic Tanakh".  EXEMPT, because they are reference tags
  rather than sentences: citation labels and the captions/headings built on them ("Simanim
  Tiqqun p. 83: the Exodus main Decalogue in the elyon"), ``img alt`` text, and image filenames.
* Rendered prose uses the **real Unicode em dash** ``—`` (U+2014), not ASCII ``--`` (``--`` is
  fine in code/comments/docstrings, like this one).
* **Never open an English sentence with a Hebrew word** (Ben, 2026-07-25).  "תרצח is that same
  alternation…" became "With תרצח, we have that same alternation…"; give the sentence an English
  runway and let the Hebrew arrive inside it.  A sentence-initial RTL run makes the reader resolve
  the direction switch before there is any English context to switch back to, and at a paragraph
  start there is not even a preceding word to anchor it.  Scoped to *English* prose: a quoted
  Biblical verse, a Hebrew-language note (``telg-doc-notes``) and the Hebrew cells of a table all
  begin with Hebrew and are untouched by this.  As of that date the trio and its sibling accgram
  pages have no other violation, so any new one is newly introduced.
* **Attribute contexts are EXEMPT from the Hebrew-letter rule, by design -- do not "fix" them.**
  Romanized "taḥton"/"elyon" is correct, and stays, inside ``img alt`` text and ``abbr title``
  text (and any similar attribute); only *visible prose* takes the Hebrew letters of bullet 1.
  Reasons: an alt/title string is announced by screen readers and copied into plain-text
  contexts, where ASCII romanization survives and a bidirectional Hebrew run does not; and an
  attribute is no place to mix alphabets.  So the trio's hover/screen-reader text being romanized
  while its prose is Hebrew-lettered is a deliberate asymmetry, NOT an inconsistency to clean up
  (settled as issue wlc-utils#65, finding T1).  Recorded here because it keeps getting re-litigated.

  **There are exactly TWO exempt registers: attributes and internal keys.**  Compact *notation*
  in visible prose is NOT a third one -- an axis gloss like ``(two books x TAHTON/ELYON x
  m-trad/p-trad)`` is visible prose and takes the Hebrew letters via the constants, however
  terse or schematic it looks.  (Only the strand words are governed; ``m-trad``/``p-trad`` are
  tradition abbreviations, not strand names, and stay as they are.)

Tested by ``tests/test_printed_decalogue_simanim.py`` and ``tests/test_printed_decalogue_page.py``
(plus the tree-wide ``tests/test_transliterations.py``).
"""

from __future__ import annotations

from accgram import printed_decalogue as pd
from accgram.uni_to_marks import is_base_letter

# Codepoints of the two marks we detect by presence (not by the _ACCENT_NAMES table).
_CP_SOF_PASUQ = "\N{HEBREW PUNCTUATION SOF PASUQ}"
_CP_METEG = "\N{HEBREW POINT METEG}"

# Romanized accent/mark names -- the single spelling used everywhere on both pages, so a name
# can neither drift nor be retyped.  Referenced both by _ACCENT_NAMES (the codepoint->name
# derivation table) and by the rendered prose of both pages; the tree-wide transliteration
# denylist (tests/test_transliterations.py) still enforces the spelling of the literals here.
# The x-form romanizations of the sound ח are written with precomposed h-with-dot-below U+1E25.
ROM_PASHTA = "pashta"
ROM_TIPEHA = "tipeḥa"
ROM_ETNAHTA = "etnaḥta"
ROM_REVIA = "revia"
ROM_SEGOLTA = "segolta"
ROM_SILLUQ = "silluq"
ROM_SOF_PASUQ = "sof pasuq"
ROM_METEG = "meteg"
ROM_MAQAF = "maqaf"
ROM_LEGARMEH = "legarmeh"
ROM_PASEQ = "paseq"
# The Shabbat-commandment accents: these fall outside the אנכי…עבדים span _ACCENT_NAMES derives,
# and are named only in the Koren page's Deuteronomy prose (issue wlc-utils#66) and the Simanim page's
# Shabbat scope note, where the p-trad/m-trad also diverge -- on the three signal words, p-trad
# geresh/revia/zaqef qatan against m-trad pazer/telisha gedolah/revia.
ROM_GERESH = "geresh"
# "zaqef", not "zaqef qatan" (Ben, 2026-07-29): "it is widely understood to be 'qatan by
# default', somewhat analogously to the way that qamats is widely understood to be gadol by
# default".  The constant keeps its full name, since that is the accent it stands for; only what
# a reader sees is shortened.  No page these strands feed names the zaqef gadol, so nothing here
# is left ambiguous by the shortening.
ROM_ZAQEF_QATAN = "zaqef"
ROM_PAZER = "pazer"
ROM_TELISHA_GEDOLAH = "telisha gedolah"
# Named only on the maqaf-nonfinal-accents page, whose accent-pair table reaches every pair that
# occurs on a chanted word of MAM's prose verses and so needs a name for marks the trio never
# meets.  The gershayim is named there in the note saying which words the table leaves out.
ROM_DARGA = "darga"
ROM_GERSHAYIM = "gershayim"
# The other name a geresh goes by when the chanted word it is on is stressed on its last
# syllable.  Named only where that page explains the abbreviated cell; the trio never needs it,
# and it is NOT a synonym to reach for -- see that explanation for why.
ROM_AZLA = "azla"
# Named only in the Simanim page's Simanim *Tanakh* verdict table (issue wlc-utils#69, Result 8), for the
# one divergence that agrees with neither תחתון strand: a qadma on ויום where every תחתון strand
# has a pashta.
ROM_QADMA = "qadma"
# Named in the Simanim page's grammaticality prose (issue wlc-utils#52): p. 246 has accents on both atoms
# of לא־תעשה, and its munax on the joined לא -- where every taxton strand has a meteg and no
# accent, and every elyon strand has לא as a free chanted word with a munax of its own -- makes
# one conjunctive too many before the pashta.  The same munax one chanted verse earlier, before a
# tevir, costs nothing.  The per-strand facts are re-derived from the vendored strands by that
# page's _pin_lo_taase_strand_facts; the sentence this comment echoes said "all eight strands
# have a meteg and no accent" until 2026-07-29, which is false of the four elyon strands (item 1
# of doc/review-findings-2026-07-29.md).
ROM_MUNAX = "munaḥ"
ROM_TEVIR = "tevir"
# Named only on the maqaf-nonfinal-accents page: the secondary mahapakh of ITM §241 is the last
# entry of Yeivin's prose closed list, which that page prints in full.  A ``ROM_OLEH_WEYORED``
# stood beside it for that page's poetic section and went when the section was cut back to a
# single paragraph (issue wlc-utils#83) -- add it back if the oleh-we-yored is ever named in prose again.
ROM_MAHAPAKH = "mahapakh"
# Named in the verdict cells that state a maqaf difference from both sides: where an edition binds
# an atom its Wikisource strand leaves free, the accent the strand has on that free atom is a
# merkha, and naming it is what keeps the difference from reading as a one-sided absence.
ROM_MERKHA = "merkha"
# The two vowels of the pausal alternation (see ``resolve_pausal``), named in the main page's
# appendix.  Vowels are not accents, but the same single-sourcing rule applies: the appendix's
# vocalization table and its pausal table both name them, and they must not drift apart.
ROM_QAMATS = "qamats"
ROM_PATAX = "pataḥ"

# Compound readings that recur verbatim in the prose (U+2026 ellipsis / U+2013 en dash between).
ROM_PASHTA_ETNAHTA = f"{ROM_PASHTA}…{ROM_ETNAHTA}"  # the merged manuscript תחתון
ROM_TIPEHA_ETNAHTA = f"{ROM_TIPEHA}–{ROM_ETNAHTA}"  # the ordinary/printed תחתון opening
ROM_TIPEHA_SILLUQ = (
    f"{ROM_TIPEHA}…{ROM_SILLUQ}"  # the manuscript עליון (standalone verse)
)
ROM_SILLUQ_SOF_PASUQ = f"{ROM_SILLUQ} + {ROM_SOF_PASUQ}"  # the standalone-verse close

# The accent codepoints that fall on the chanted words these pages derive an accent for -- the first
# Decalogue span's two boundary words, plus the two pausal words of ``resolve_pausal`` (geresh is
# there for מתחת in the עליון) -- mapped to the romanizations above.  U+05BD (meteg/silluq) is
# deliberately absent: it is not an accent, and is resolved to silluq only in
# verse-final position (see ``_accent_of`` and CLAUDE.md on meteg-vs-silluq).
_ACCENT_NAMES: dict[str, str] = {
    "\N{HEBREW ACCENT PASHTA}": ROM_PASHTA,
    "\N{HEBREW ACCENT TIPEHA}": ROM_TIPEHA,
    "\N{HEBREW ACCENT ETNAHTA}": ROM_ETNAHTA,
    "\N{HEBREW ACCENT REVIA}": ROM_REVIA,
    "\N{HEBREW ACCENT GERESH}": ROM_GERESH,
}

# The vowels ``_vowel_and_accent`` recognizes: just the two the pausal alternation turns on.  A
# third vowel showing up in that position would be a data change worth failing on, not something
# to name silently, so this table stays minimal on purpose.
_VOWEL_NAMES: dict[str, str] = {
    "\N{HEBREW POINT QAMATS}": ROM_QAMATS,
    "\N{HEBREW POINT PATAH}": ROM_PATAX,
}

# Base-letter skeletons of the four chanted words the אנכי…מצותי span is laid out over, single-sourced
# here for all three pages and located within a strand's span by matching letters.
#
# עבדים and על־פני are the span's two SIGNAL WORDS: their accent pair is different in each of the
# four strands, so the pair alone says which strand a text has (resolve_readings checks that
# pairwise distinctness live).  Each sits mid-verse in some strands and verse-finally in others,
# and that is exactly what it signals.
#
# על־פני is a maqaf compound, and the compound is the whole chanted word here -- which is why its skeleton
# runs both letter-groups together as עלפני, and why ``_accent_of`` reads the accent off the
# compound rather than off a half.  Name the signal word על־פני, NEVER a bare פני: no page should
# name פני and then qualify that it is really part of על־פני (Ben, 2026-07-19).
#
# אנכי and מצותי are the span's shared FRAME, not signal words: every strand starts at אנכי (never
# verse-finally) and closes a chanted verse at מצותי, so neither tells any two strands apart.
ANOKHI = "אנכי"
AVADIM = "עבדים"
AL_PENEI = "עלפני"
MITSVOTAI = "מצותי"

# The span's other pausal word (``resolve_pausal``): מתחת, in ואשר בארץ מתחת.  It occurs TWICE in
# the second commandment -- again in מתחת לארץ, a few words later -- and this is the first, which is
# the one ``_find_word`` returns.  The second one has neither of the two accents the pins expect
# (merkha in the תחתון, munax in the עליון), so picking up the wrong one would fail the build
# rather than mis-render.  על־פני, the other pausal word, is already AL_PENEI above: it does double
# duty as a signal word.
MITAXAT = "מתחת"


# The two chant-strands (טעם) are named in Hebrew letters throughout the rendered prose --
# תחתון / עליון -- and are NEITHER transliterated NOR translated (see the module docstring).
# The romanized forms "taxton"/"elyon" survive only as internal keys (``READING_SPECS`` /
# ``STRUCTURE`` names).  The two strand words are plain Hebrew string constants, substituted
# directly into the prose (including inside f-strings) rather than wrapped in a lang="he" <span>.
TAHTON = "תחתון"
ELYON = "עליון"
_STRAND_HEB: dict[str, str] = {"taḥton": TAHTON, "elyon": ELYON}


# The one-sentence statement of what the four strands most strikingly disagree about, shared
# VERBATIM by all three pages of the trio (main + the Simanim and Koren pages) so it cannot
# drift between them.  Plain ``str``, not HTML: splice it into a contents tuple.
#
# Why this span and not the older "is אנכי…עבדים an entire chanted verse or only the start of
# one?": that framing asked a yes/no question and pinned it on the p-trad/m-trad axis, but the
# answer doesn't split on that axis at all -- each tradition says yes with one strand and no with
# the other (m-trad עליון and p-trad תחתון make it its own verse; m-trad תחתון and p-trad עליון
# run it on).  Widening to אנכי…מצותי states the real, four-way difference: over this span the
# strands divide into 5 (p-trad תחתון), 4 (m-trad תחתון), 2 (m-trad עליון) and 1 (p-trad עליון)
# chanted verses -- no two alike.  The span is principled, not chosen to taste: every strand has a
# verse boundary at מצותי, and it is exactly the p-trad עליון's entire first verse (see
# ``STRUCTURE``), i.e. the smallest span that contains all four strands' disagreement.
MOST_STRIKING = (
    "The most striking difference between the four strands is how they divide up the span"
    " אנכי…מצותי into chanted verses. (This span is typically identified as comprising the"
    " first two Commandments.)"
)


# The shared description of the Deuteronomy Shabbat commandment's three signal words, used
# verbatim by both satellite pages (Simanim and Koren) where each shows its own scan of that
# commandment.  Plain ``str``, not HTML: splice it into a contents tuple.
#
# THE COMPLEMENTARY-JOBS DOCTRINE (do not collapse the two signal-word sets into one claim).
# The span's own signal words -- עבדים and על־פני -- carry a strong claim: their accent pair is
# unique to each of the four strands, so the pair places a text among them.  But that claim is
# about the four IDEALIZED strands as Hebrew Wikisource defines them.  A real edition need not
# follow one strand purely: Simanim's Tiqqun follows the p-trad תחתון's chanted verse boundaries
# throughout, yet has the m-trad accents at the Shabbat commandment of its Deuteronomy appendix
# Decalogue.  The span pair cannot catch that -- it is an accents-only departure that moves no
# boundary the pair reads.  The Shabbat trio can, because it compares accents at a commandment
# the two traditions divide into chanted verses identically.  So: עבדים and על־פני place a text
# among the four strands within אנכי…מצותי, while the Shabbat trio tells p-trad accents from
# m-trad accents where an edition can stray from its nominal tradition.  Neither makes the other
# redundant, and no page may imply that it does.
SHABBAT_SIGNAL_SHORTHAND = (
    "three signal words highlighted — not the only chanted words the two traditions accent"
    " differently, but three disjunctively accented ones that make a handy shorthand"
    " for telling the p-trad from the m-trad"
)


# Where maqaf sits relative to the accents, and what the verdicts therefore measure, stated to
# the reader verbatim on all three pages of the trio -- the hub where it first says two editions
# put their maqafs differently, and each satellite where it introduces its own per-Decalogue
# verdict table.  Plain ``str``, not HTML: splice it into a contents tuple.
#
# WHY IT IS SAID AT ALL (2026-07-25 claim audit, finding 3).  The trio used "every accent" two
# ways at once.  Koren's Exodus appendix Decalogue was credited with "Every accent. The only two
# differences are of word division", while the summary directly under the same table counted that  # prose-ok: quotes the replaced convention
# very Decalogue as the one of four that "does NOT follow its strand in every accent" -- and the
# Deuteronomy appendix one was credited with "no difference anywhere" although it joins לא־תעשה
# into a maqaf compound where its Wikisource strand sets the two atoms apart.  Both readings were
# available and the page contradicted itself.
#
# WHY THIS ANSWER AND NOT THE FIRST ONE (Ben, 2026-07-25).  That contradiction was first settled
# the other way, by declaring a maqaf difference to be no accent difference at all -- a second
# ledger, kept apart from the accents.  That convention was wrong, and wrong in a way the repo
# had already ruled on: ``supplied_marks``' punctuation intro tells its own reader that maqaf is
# "so tightly coupled" to the lack of an accent "that detangling accents and detangling
# punctuation can be regarded as one and the same activity", and ``printed_decalogue_taxton_diff``
# already counts a maqaf difference as one ordinary difference SITE.  The real problem the old
# convention solved was double counting -- reporting a split compound as a division AND as a new
# accent -- and the honest fix is that those were never two facts.  One atom's marking changed.
# So: one scale, maqaf at the bottom of it, each difference counted once at the atom it sits on.
#
# WHY IT NAMES ATOMS AND CHANTED WORDS (issue wlc-utils#81).  A maqaf sits on an ATOM and joins it to the
# next; what the two of them become is one CHANTED WORD.  An earlier wording called both of those
# "the word", so the one sentence that exists to draw the distinction used a single noun for both
# sides of it.  This is also the trio's introduction of "atom" to the reader -- the appositive
# gloss is why it can be used bare on the pages afterwards.
MAQAF_IS_THE_LAST_RUNG = (
    "One thing to settle first, since it decides what these verdicts mean. A maqaf belongs on the"
    " same scale"
    " as the accents, at the bottom of it: it separates the atom it sits on — one written word —"
    " from the next even less than a conjunctive accent does, binding the two into a single"
    " chanted word, the unit an accent marks. So"
    " where an edition has a maqaf on an atom and its Wikisource strand a conjunctive accent, or"
    " the other way about, that is one difference in how that atom is marked — an exchange one"
    " rung deep, counted once and not twice as a regrouping plus an accent. It is, though, the"
    " mildest difference there is, and that is what these verdicts measure: how far down the"
    " scale each Decalogue's agreement with that strand reaches — the chanted verse boundaries,"
    " then the disjunctive skeleton, then the conjunctives, then the maqafs."
)


def render_reading_name(name: str) -> tuple[object, ...]:
    """A reading name like ``"m-trad taḥton"`` rendered with its strand word in Hebrew
    letters: ``("m-trad ", "תחתון")``.  The tradition half stays English."""
    tradition, strand = name.split()
    return (tradition + " ", _STRAND_HEB[strand])


# --------------------------------------------------------------------------- #
# Deriving the four readings live from the vendored data
# --------------------------------------------------------------------------- #
def base_skeleton(word: str) -> str:
    return "".join(ch for ch in word if is_base_letter(ch))


def _accent_index_and_name(word: str) -> tuple[int, str]:
    """Where the word's accent mark sits, and its romanized name.  The index is what
    ``_vowel_and_accent`` needs in order to find the vowel that shares the accent's letter;
    ``_accent_of`` wants only the name."""
    for i, ch in enumerate(word):
        name = _ACCENT_NAMES.get(ch)
        if name is not None:
            return i, name
    if _CP_SOF_PASUQ in word and _CP_METEG in word:
        return word.index(_CP_METEG), ROM_SILLUQ
    raise ValueError(f"no recognized boundary accent on {word!r}")


def _accent_of(word: str) -> str:
    """The accent on one pointed word, as a romanized name derived from its marks.

    A word has at most one of the boundary accents we care about.  U+05BD is not an
    accent, but the same glyph functions as *silluq* on the verse-final chanted word
    (the one carrying *sof pasuq*); so a sof-pasuq word whose only accent-like mark is U+05BD
    is reported as silluq.  Never called on a non-verse-final U+05BD (that is an ordinary
    meteg -- see CLAUDE.md)."""
    return _accent_index_and_name(word)[1]


def _vowel_and_accent(word: str) -> tuple[str, str]:
    """The (vowel, accent) pair of one pointed word, where "the vowel" is the one on the SAME
    letter as the accent -- which is the only vowel the pausal alternation is about.

    Reading it off the accent's own letter is what makes this safe on a word with more than one
    of the two vowels in the table: עַל־פָּנָֽי has a qamats under the pe as well as the one under
    the accented nun, and only the second is at issue.  So: walk back from the accent mark to the
    base letter it sits on, and take the vowel found in between.  Raises unless exactly one
    turns up, so an unforeseen pointing fails the build instead of being reported as a vowel it
    is not."""
    accent_i, accent = _accent_index_and_name(word)
    vowels = []
    for ch in reversed(word[:accent_i]):
        if is_base_letter(ch):
            break
        name = _VOWEL_NAMES.get(ch)
        if name is not None:
            vowels.append(name)
    if len(vowels) != 1:
        raise ValueError(
            f"expected exactly one vowel on the accented letter of {word!r}, found {vowels}"
        )
    return vowels[0], accent


def _find_word(words: tuple[str, ...], skeleton: str) -> str:
    for word in words:
        if base_skeleton(word) == skeleton:
            return word
    raise ValueError(f"no word with skeleton {skeleton!r} in {words!r}")


def _span_verses(vr: pd.VersionResult) -> list[pd.ChantedVerseResult]:
    """The leading chanted verses covering the אנכי…מצותי span: every verse through the first
    one whose last word is מצותי.  Every strand closes a chanted verse there (that is what makes
    the span principled -- see MOST_STRIKING), so this is well defined for all eight readings;
    an AssertionError on drift, in the style of ``resolve_readings``."""
    out: list[pd.ChantedVerseResult] = []
    for cv in vr.chanted_verses:
        out.append(cv)
        if base_skeleton(cv.words[-1]) == MITSVOTAI:
            return out
    raise AssertionError(
        f"{vr.book} {vr.reading} {vr.tradition}: no chanted verse ends at {MITSVOTAI!r} "
        "-- the vendored readings drifted"
    )


class Reading:
    """One of the four ways the opening Decalogue span is accented, resolved from the data."""

    def __init__(self, name: str, vr: pd.VersionResult):
        first = vr.chanted_verses[0]
        self.name = name  # romanized, e.g. "m-trad taxton"
        # The whole first chanted verse's word tuple, so page 1's range cells can read
        # first / mid (עבדים) / last words directly off the data.
        self.first_verse_words = first.words
        self.anokhi_word = first.words[0]
        self.avadim_word = _find_word(first.words, AVADIM)
        self.anokhi_accent = _accent_of(self.anokhi_word)
        self.avadim_accent = _accent_of(self.avadim_word)
        # The whole אנכי…מצותי span: its chanted verses, its words flattened, and the letter
        # skeletons of the words that END those verses -- the last being the set page 1's table
        # colors red, so a cell is red exactly where its strand closes a chanted verse.
        self.span_verses = _span_verses(vr)
        self.span_words = tuple(w for cv in self.span_verses for w in cv.words)
        self.span_end_skels = frozenset(
            base_skeleton(cv.words[-1]) for cv in self.span_verses
        )
        # The second signal word, על־פני, and its accent -- silluq where the strand closes a
        # chanted verse there, revia where it runs on.  Paired with avadim_accent it identifies
        # the strand (resolve_readings checks the four pairs are pairwise distinct).
        self.penei_word = _find_word(self.span_words, AL_PENEI)
        self.penei_accent = _accent_of(self.penei_word)
        # How many chanted verses this strand splits the Exodus Decalogue into, and the
        # letter skeleton of its first chanted verse's last word (its span endpoint).
        self.n_verses = len(vr.chanted_verses)
        self.first_verse_end = base_skeleton(first.words[-1])


# (display name, ex reading, ex data-tradition, expected אנכי, expected עבדים, expected על־פני) --
# the expected accents pin the live derivation so a data change that moved a boundary accent would
# fail the build rather than silently mis-render.  The last two are the span's signal words; their
# PAIR is what identifies a strand, and resolve_readings additionally checks that the four pairs
# here really are pairwise distinct rather than trusting the table to stay that way.  The first
# verse's span + verse count are pinned separately in STRUCTURE; display extras live in the table
# renderers, keyed by name.
#
# NB: the third element is the DATA lookup key (matched against vr.tradition in resolve_readings),
# which the source emits as "manuscript"/"printed" -- NOT the "m-trad"/"p-trad" display shorthand.
# Keep it in the source's spelling; only the display name (first element) uses the shorthand.
READING_SPECS = (
    ("m-trad taḥton", "taxton", "manuscript", ROM_PASHTA, ROM_ETNAHTA, ROM_SILLUQ),
    ("m-trad elyon", "elyon", "manuscript", ROM_TIPEHA, ROM_SILLUQ, ROM_REVIA),
    ("p-trad taḥton", "taxton", "printed", ROM_TIPEHA, ROM_SILLUQ, ROM_SILLUQ),
    ("p-trad elyon", "elyon", "printed", ROM_PASHTA, ROM_REVIA, ROM_REVIA),
)

# Per-strand opening structure: (first-verse span as short right-to-left notation, the
# letter skeleton of that first verse's last word, the number of chanted verses the
# strand divides the Exodus Decalogue into).  ``end_skel`` and ``n_verses`` are pinned
# against the vendored data in resolve_readings so a moved boundary fails the build rather
# than silently mislabelling.  (span endpoints from the data: אנכי…על־פני / …עבדים / …מצותי.)
STRUCTURE: dict[str, tuple[str, str, int]] = {
    "m-trad taḥton": ("אנכי…על־פני", "עלפני", 12),
    "m-trad elyon": ("אנכי…עבדים", "עבדים", 10),
    "p-trad taḥton": ("אנכי…עבדים", "עבדים", 13),
    "p-trad elyon": ("אנכי…מצותי", "מצותי", 9),
}


def _signal_pair(vr: pd.VersionResult) -> tuple[str, str]:
    """The (עבדים, על־פני) accent pair of one reading -- the pair that identifies its strand.
    Used to check the Deuteronomy readings against their Exodus counterparts without building a
    whole ``Reading`` for each (the pages tabulate Exodus; the claim covers both books).
    """
    span_words = tuple(w for cv in _span_verses(vr) for w in cv.words)
    return (
        _accent_of(_find_word(span_words, AVADIM)),
        _accent_of(_find_word(span_words, AL_PENEI)),
    )


def resolve_readings(results: list[pd.VersionResult]) -> list[Reading]:
    by_key = {(vr.book, vr.reading, vr.tradition): vr for vr in results}
    readings: list[Reading] = []
    for name, reading, tradition, exp_anokhi, exp_avadim, exp_penei in READING_SPECS:
        r = Reading(name, by_key[("ex", reading, tradition)])
        derived = (r.anokhi_accent, r.avadim_accent, r.penei_accent)
        expected = (exp_anokhi, exp_avadim, exp_penei)
        if derived != expected:
            raise AssertionError(
                f"{name}: derived {derived} from the data, "
                f"expected {expected} -- the vendored readings drifted"
            )
        _, end_skel, n_verses = STRUCTURE[name]
        if (r.first_verse_end, r.n_verses) != (end_skel, n_verses):
            raise AssertionError(
                f"{name}: derived first-verse end {r.first_verse_end!r} / {r.n_verses} verses "
                f"from the data, expected {end_skel!r} / {n_verses} -- the vendored readings drifted"
            )
        # The pages claim the (עבדים, על־פני) pair identifies the strand in BOTH books, but
        # tabulate only Exodus; check the Deuteronomy counterpart derives the same pair.
        #
        # An editorial decision this check may prompt someone to reopen: the m-trad elyon's
        # Deuteronomy opening accents are a MAM editorial reconstruction.  The pages deliberately
        # do NOT mention that -- Ben's call, 2026-07-19: don't get into it.  It changes nothing
        # here (the reconstructed accents are the data, and the check below passes on them);
        # it is purely a question of what the rendered prose discusses.  Settled; don't re-add.
        dt_pair = _signal_pair(by_key[("dt", reading, tradition)])
        if dt_pair != (r.avadim_accent, r.penei_accent):
            raise AssertionError(
                f"{name}: Deuteronomy signal pair {dt_pair} differs from Exodus's "
                f"{(r.avadim_accent, r.penei_accent)} -- the vendored readings drifted"
            )
        readings.append(r)
    # The page's headline claim: no two strands share the signal pair, so the pair alone places a
    # text among the four.  Checked live rather than trusted to READING_SPECS staying distinct.
    pairs = {(r.avadim_accent, r.penei_accent): r.name for r in readings}
    if len(pairs) != len(readings):
        raise AssertionError(
            "the four strands no longer have pairwise-distinct (עבדים, על־פני) signal pairs: "
            f"{[(r.name, r.avadim_accent, r.penei_accent) for r in readings]} "
            "-- the vendored readings drifted"
        )
    return readings


# --------------------------------------------------------------------------- #
# The pausal alternation at על־פני and מתחת
# --------------------------------------------------------------------------- #
# Why the main page's appendix wants these two words at all.  The appendix's one Exodus difference
# between the two תחתון strands is a VOWEL -- qamats m-trad against patax p-trad at תרצח, on the
# same tipexa -- and that pair of vowels is not arbitrary: it is the pausal alternation, the
# general rule for which (Yeivin ITM §199) is that the pausal vowel goes with etnaxta and silluq
# and the contextual one with every other accent.  על־פני and מתחת are where the Decalogue shows
# that rule doing exactly what it says: at both, the תחתון has the pausal qamats under the heavier
# accent its own verse division gives the word, and the עליון the contextual patax under a lighter
# one.  So the appendix can say what makes תרצח the odd case -- there the two strands have the SAME
# accent, so the rule does not decide the vowel and the two traditions differ.
#
# The pins below are what license the appendix's claim that neither of these two words is a
# p-trad-vs-m-trad difference: ``resolve_pausal`` derives the (vowel, accent) pair at both words
# from ALL EIGHT readings and requires each to match its strand's pin, so the claim is checked on
# every generation rather than asserted once.  Keyed by (skeleton, reading) -- the vowel and the
# accent both turn on the strand alone, identically in Exodus and Deuteronomy and in both
# traditions, which is the whole point.
PAUSAL_SKELETONS: tuple[str, ...] = (AL_PENEI, MITAXAT)
_PAUSAL_PINS: dict[tuple[str, str], tuple[str, str]] = {
    (AL_PENEI, "taxton"): (ROM_QAMATS, ROM_SILLUQ),
    (AL_PENEI, "elyon"): (ROM_PATAX, ROM_REVIA),
    (MITAXAT, "taxton"): (ROM_QAMATS, ROM_ETNAHTA),
    (MITAXAT, "elyon"): (ROM_PATAX, ROM_GERESH),
}

# The data's own reading keys -> the Hebrew strand words.  Distinct from _STRAND_HEB, which is
# keyed by the display names, which spell that strand's name with an h-with-dot-below where the
# vendored source spells it "taxton".
_STRAND_HEB_BY_READING: dict[str, str] = {"taxton": TAHTON, "elyon": ELYON}


class PausalForm:
    """One strand's pointed form of one of the two pausal words, with the vowel and accent on its
    accented letter.  ``strand`` is already the Hebrew word, ready for the prose."""

    def __init__(self, strand: str, word: str, vowel: str, accent: str):
        self.strand = strand
        self.word = word
        self.vowel = vowel
        self.accent = accent


def resolve_pausal(results: list[pd.VersionResult]) -> tuple[PausalForm, ...]:
    """The four forms the appendix's pausal table displays -- על־פני then מתחת, תחתון before
    עליון in each -- taken from the two Exodus manuscript readings, but only after every one of
    the eight readings has been checked to derive the same (vowel, accent) at both words.

    That check is the claim, not a formality: the appendix says these two words differ by strand
    and not by tradition, and the eight-way agreement is what makes it true.  AssertionError on
    drift, in the style of ``resolve_readings``."""
    forms: dict[tuple[str, str], PausalForm] = {}
    for vr in results:
        span_words = tuple(w for cv in _span_verses(vr) for w in cv.words)
        for skeleton in PAUSAL_SKELETONS:
            word = _find_word(span_words, skeleton)
            derived = _vowel_and_accent(word)
            expected = _PAUSAL_PINS[(skeleton, vr.reading)]
            if derived != expected:
                raise AssertionError(
                    f"{vr.book} {vr.reading} {vr.tradition}: derived {derived} at {skeleton!r} "
                    f"({word!r}), expected {expected} -- the vendored readings drifted"
                )
            if (vr.book, vr.tradition) == ("ex", "manuscript"):
                forms[(skeleton, vr.reading)] = PausalForm(
                    _STRAND_HEB_BY_READING[vr.reading], word, *derived
                )
    ordered = [
        (skeleton, reading)
        for skeleton in PAUSAL_SKELETONS
        for reading in ("taxton", "elyon")
    ]
    missing = [key for key in ordered if key not in forms]
    if missing:
        raise AssertionError(
            f"no Exodus manuscript reading supplied {missing} -- the vendored readings drifted"
        )
    return tuple(forms[key] for key in ordered)


# The rest of what the appendix says about תרצח, pinned the same way.  Two claims live here that
# the vocalization table alone does not carry: that the two תחתון strands' split is a vowel and
# nothing else (the same tipexa in both), and that it is confined to the תחתון -- in the עליון the
# word ends the two-word chanted verse לא תרצח, so it carries silluq and BOTH traditions have the
# pausal qamats on it.  That second one is what makes תרצח the odd case beside על־פני and מתחת, so
# it is checked rather than typed.  Unlike the two pausal words, תרצח falls outside the אנכי…מצותי
# span, so ``check_tirtsax`` scans a reading's whole Decalogue for it.
#
# SAY WHAT ENDS THE VERSE, NOT WHAT IS ONE (Ben, 2026-07-25).  This prose first read "in the עליון
# the word is a chanted verse of its own", which is flatly false: the verse is לא תרצח, two
# separately accented words (the same reason _VOWEL_DIFF_ROWS names the word bare rather than
# naming the pair).  A word ENDS a chanted verse; only a one-word verse would BE one.  The same
# slip is easy at על־פני, which likewise ends a verse in two strands without being one.
TIRTSAX = "תרצח"
_TIRTSAX_PINS: dict[tuple[str, str], tuple[str, str]] = {
    ("taxton", "manuscript"): (ROM_QAMATS, ROM_TIPEHA),
    ("taxton", "printed"): (ROM_PATAX, ROM_TIPEHA),
    ("elyon", "manuscript"): (ROM_QAMATS, ROM_SILLUQ),
    ("elyon", "printed"): (ROM_QAMATS, ROM_SILLUQ),
}


def check_tirtsax(results: list[pd.VersionResult]) -> None:
    """Check all eight readings' vocalization of תרצח against ``_TIRTSAX_PINS``.  Raises rather
    than let the appendix's prose about that word outlive the data it describes."""
    for vr in results:
        words = tuple(w for cv in vr.chanted_verses for w in cv.words)
        word = _find_word(words, TIRTSAX)
        derived = _vowel_and_accent(word)
        expected = _TIRTSAX_PINS[(vr.reading, vr.tradition)]
        if derived != expected:
            raise AssertionError(
                f"{vr.book} {vr.reading} {vr.tradition}: derived {derived} at {TIRTSAX!r} "
                f"({word!r}), expected {expected} -- the vendored readings drifted"
            )
