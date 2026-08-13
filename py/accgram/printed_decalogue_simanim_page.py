r"""Generate gh-pages/wlc/accgram/printed-decalogue-simanim.html -- does Simanim's Tiqqun follow
the printed or the manuscript Decalogue tradition?  Answer: the printed tradition (issue wlc-utils#62) --
precisely, it follows the p-trad's chanted verse boundaries, but not its every cantillation
detail: the Shabbat commandment of its Deuteronomy taḥton (appendix) Decalogue has the m-trad
accents, an accents-only divergence that moves no chanted verse boundary (see ``_conclusion``).

Companion to ``printed_decalogue_page`` (issue wlc-utils#52, which grammar-checks the printed vs
manuscript Decalogue accentuations and lays out the four cantillation strands).  This page ports
two research notes -- formerly issue wlc-utils#56 comments -- into a versioned, reviewable document:

  * **p. 83** (main Decalogue, *elyon*): SimTiq's side-margin note on the Exodus (Yitro)
    Decalogue first span אנכי...עבדים.  Its default (בפנים) elyon reading ends that span on a
    *revia* (the merged, 9-verse printed structure); "some books" instead give אנכי...עבדים its
    own verse (silluq + *sof pasuq* at עבדים) to keep ten distinct commandments.
  * **p. 246** (appendix, *taḥton*): the mirror footnote, contrasting בטעם רגיל (= printed
    taḥton: אנכי...עבדים as its own verse, *sof pasuq* at עבדים) with כתר אר״ץ (= manuscript
    taḥton: pashta...etnaḥta, merged).

What actually establishes the answer is not these notes but SimTiq's *body text*: its main
Decalogue (p. 83) and appendix Decalogue (p. 246) are compared, by the author, against what Hebrew
Wikisource records as the printed tradition, and they match.  That body text is asserted here,
not reproduced.  The two notes are secondary -- kept for the more-for-fun question of
how aware SimTiq is of having made the older, printed-tradition choice.

Since issue wlc-utils#69 the finding rests on more than that comparison.  All EIGHT Decalogues on this page
-- the Tiqqun's four and the Simanim *Tanakh*'s four -- have a committed hand transcription of
every printed accent (``in/accgram/edition_transcriptions/simtiq_*.txt`` and ``simtan_*.txt``),
diffed against the vendored strand and pinned by
``tests/test_edition_transcriptions.py``.  ``_tiqqun_verdict_table``
and ``_tanakh_verdict_table`` render them, one row per Decalogue -- never one per edition, since
p. 247's Shabbat departure and pp. 208-209's exact agreement cannot share a sentence.

Each table's LAST column is issue wlc-utils#52's question asked of these eight: fed through accgram's
prose checker, is what the page prints grammatical, and as grammatical as the Wikisource strand
it follows?  The cells come live from ``transcription_verdict_column`` (shared with the Koren
page) so no row can claim a verdict the checker does not give.  Six of the eight give their
Wikisource strand's verdicts exactly.  Two do not, and the two want different prose.

p. 246 is the primary case, and the prose after the Tiqqun table has to hold two true things
together: no divergence of its reaches a disjunctive, so its skeleton is intact, AND one of its
chanted verses is ungrammatical where its Wikisource strand is clean.
Say the second without qualification: the accent sequence is ungrammatical, not merely rejected
by this checker, and that much would be visible from the edition alone, whose accentuation is
otherwise grammatical throughout.  Do NOT write the converse THERE -- that the edition is in error, or that the
passage should not be chanted as printed.  Ungrammatical is not the same as wrong, and p. 246's
extra munaḥ on the joined atom of לא־תעשה is a well-formed accent in a chain the grammar finds
too long: three servi before the pashta where it takes two.  A tradition that chants it is not
ruled out by anything on the page.

p. 298 is the second case, and it is the one where the evidence does reach that far: Ben's
decision, 2026-08-03, is that the page says the qadma there is very likely the edition's error.
What separates it from p. 246 is that neither primary has any configuration that would put that
mark there.  ITM §223 and CoS Ch. 5 §4 both restrict the metigah to the chanted word of the zaqef, and
ויום is one chanted word and השביעי another, with a space and not a maqaf between them -- so the
qadma is no metigah, and every תחתון strand has a pashta in its place.  p. 246's mark is a legal
accent in a chain that runs too long; p. 298's is a mark neither book's rules reach.  So the ban
above is scoped to p. 246 and does not travel to p. 298.

TWO SENSES OF "TRANSCRIPTION", KEPT APART (issue wlc-utils#69 decision 3a).  This page had the word first
for the two *note* transcriptions -- the hand-set pointed Hebrew of the p. 83 and p. 246 notes,
double-checked against the committed scans, and still the only hand-set Hebrew in this module.
The accent transcriptions above are the other sense: a token per printed accent, machine-diffed,
and never displayed as Hebrew.  On first mention call those "hand transcriptions of the printed
accents"; where both senses appear in one section, the older one is "the note transcriptions".

The four cantillation strands of the opening אנכי...מצותי span are derived live from the vendored
``in/accgram/printed_decalogue_teamim.json`` by the shared ``printed_decalogue_strands`` module
and tabulated on the companion page; this page links to that table rather than duplicating it.

The trio frames that span around its two SIGNAL WORDS, עבדים and על־פני, whose accent pair
uniquely identifies which of the four strands a text has.  This page is where the limits of that
claim show: the pair identifies the four IDEALIZED Wikisource strands, and Simanim's Tiqqun is
not pure -- its Deuteronomy taḥton has the m-trad accents at the Shabbat commandment, an
accents-only departure the span pair cannot catch because it moves no chanted verse boundary.
Catching it requires GIVING the Shabbat commandment its own signal words
(``pds.SHABBAT_SIGNAL_SHORTHAND``,
where the complementary-jobs doctrine is spelled out).  So this page is the canonical example
keeping that second signal-word set load-bearing; never let a rewrite imply עבדים and על־פני
would have sufficed here.

Editorial / style conventions shared with the companion page -- bare-Hebrew strand names
תחתון / עליון (never transliterated or translated), the single-sourced ``ROM_*`` accent
romanizations, and the real-em-dash rule -- are documented on ``printed_decalogue_strands`` and
imported from it (the thin ``_TAHTON`` / ``_ELYON`` aliases below just limit prose churn; the
``_ROM_*`` ones additionally wrap each name in the italic ``span.romanized``, so they are HTML
nodes rather than strings -- see the comment at that alias block).  The conventions specific to
THIS page (keep them when editing):

* Prefer "**cantillation**" to "accentuation".
* **Three term pairs, kept strictly apart** (a recurring inconsistency -- don't regress):
  *main* vs *appendix* = the book's two parts (the running ḥumash vs the Decalogue reprinted at
  the back); *body* vs *note* = printed text vs annotation; and the two notes differ by
  placement.  Use "main" ONLY for main-vs-appendix -- pair it as "main Decalogue" /
  "appendix Decalogue", never "main text" -- and "body" ONLY for body-vs-note (so the p. 83
  note's ``בפנים`` renders as "the body", NOT "the main text").  The **p. 83** note sits in the
  **side margin** ("side-margin note"); the **p. 246** note sits in the **bottom margin**, keyed
  by an asterisk -- it is a **footnote**, so never call it a "marginal note".  For the pair, say
  "notes" (never "marginal notes").
* **Image ``alt`` text keeps romanized names** ("taḥton") on purpose -- attribute contexts are
  exempt from the Hebrew-letter rule by design; see the "Attribute contexts are EXEMPT" bullet in
  ``printed_decalogue_strands``' module docstring for the full rule and why.

Regenerate with ``main_accgram.py generate-html``; test with
``tests/test_printed_decalogue_simanim.py`` (plus the tree-wide
``tests/test_transliterations.py``).  The 2026-07-10 editorial pass that established the
conventions above kept a running edit log in gitignored scratch; every item was applied and the
durable rules were folded into this docstring, which is now their only home.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from accgram import accent_marks as am
from accgram import printed_decalogue as pd
from accgram import printed_decalogue_strands as pds
from accgram import rtms_report
from accgram import transcription_parse as tp
from accgram import transcription_verdict_column as tvc
from accgram.almost_errors_html_shared import accents_and_letters, cos, hbo, itm, link
from accgram.uni_to_marks import is_accent, is_base_letter
from wlc_cmn.utf8_io import force_utf8_io
from mb_cmn import paths
from mb_cmn import provenance

from py_html import wlc_utils_html as H
from py_html import my_html_for_img as mhi
from py_html.my_html_span_romanized import rmn

# "chanted verse boundaries", not a bare "the printed tradition": the Tiqqun's p-trad allegiance
# is exceptionless for chanted verse boundaries but not for every cantillation detail -- its
# Deuteronomy taxton Shabbat commandment has the m-trad accents (the first scope note in
# _conclusion). The title claims only the exceptionless part.
REPORT_TITLE = (
    "Simanim's Tiqqun follows the printed tradition's chanted verse boundaries"
    " for the Decalogues"
)

# _ISSUE_52 = "https://github.com/bdenckla/wlc-utils/issues/52"
# _ISSUE_56 = "https://github.com/bdenckla/wlc-utils/issues/56"
_PRINTED_DECALOGUE_PAGE = "printed-decalogue.html"
# The Koren companion. Until issue wlc-utils#69's prose pass the cross-reference ran only Koren -> Simanim,
# and on this side existed only in code comments -- so a reader of the rendered page had no way to
# reach the sibling edition's document. Both links below are the return half of a link Koren
# already makes: its p. A38 note section links to this page's p. 83 note, and its conclusion's
# scope note links here for the Shabbat departure.
_KOREN_PAGE = "printed-decalogue-koren.html"
# The four-strands table now lives on the companion page (issue wlc-utils#52); cross-references whose link
# text names the table land on its heading anchor there rather than on a local table.
_FOUR_STRANDS_HREF = f"{_PRINTED_DECALOGUE_PAGE}#four-strands"
# Link text that names the page, not the table, gets the page itself: an anchor would drop the
# reader past the companion's own intro, mid-page, which is not what "the companion page" promises.
_COMPANION_PAGE_HREF = _PRINTED_DECALOGUE_PAGE
# The companion's appendix cataloguing how the two תחתון strands differ (its heading id there,
# _TAHTON_DETAILS_ID) -- the reference for Shabbat-commandment accent details this page omits.
_TAHTON_DETAILS_HREF = f"{_PRINTED_DECALOGUE_PAGE}#tahton-details"
_P83_IMG = "img/Simanim-Tiqqun-p-083-Ex-Dec-elyon-sidenote.png"
_P246_IMG = "img/Simanim-Tiqqun-p-246-Ex-Dec-p-trad-taxton-footnote.png"
# Body-text scans (issue wlc-utils#62): the SimTiq Decalogues whose cantillation establishes the p-trad
# finding -- distinct from the two note scans above (the constant names encode strand + page).
_P83_BODY_IMG = "img/Simanim-Tiqqun-p-083-Ex-Dec-elyon.png"
_P246_BODY_IMG = "img/Simanim-Tiqqun-p-246-Ex-Dec-p-trad-taxton.png"
# Highlight rectangles in Simanim-Tiqqun-p-083 pixel space (961x664, the scan's own
# resolution = the overlay viewBox). Each Box marks a word named in the figcaption; the
# coordinates come from py/accgram/gen_highlight_picker.py (drag boxes over the words, then
# paste the exported `px` boxes here). These three mark the two signal words, עבדים and על־פני,
# plus מצותי -- the אנכי…מצותי span's shared end, marked for orientation, not as a signal (every
# strand closes a chanted verse there, so it distinguishes nothing).
_P83_BOXES: tuple[mhi.Box, ...] = (
    mhi.Box(x=800, y=145, w=161, h=71),
    mhi.Box(x=84, y=141, w=160, h=73),
    mhi.Box(x=639, y=572, w=155, h=66),
)
# Highlight rectangles in Simanim-Tiqqun-p-246 pixel space (1149x327, the scan's own
# resolution = the overlay viewBox). Mirroring the p. 83 highlights above, these two mark the
# אנכי…מצותי span's two signal words, עבדים and על־פני, both named in the figcaption. Coordinates
# come from py/accgram/gen_highlight_picker.py (drag boxes over the words, export the `px`
# boxes). Note the p. 246 scan is a different size than the p. 83 one (1149x327 vs 961x664).
_P246_BOXES: tuple[mhi.Box, ...] = (
    mhi.Box(x=942, y=218, w=192, h=77),
    mhi.Box(x=114, y=201, w=183, h=87),
)
# Highlight rectangles in Simanim-Tanakh-p-119 pixel space (972x259, the scan's own
# resolution = the overlay viewBox). Mirroring the p. 83 / p. 246 highlights above, these
# two mark the same two signal words as the p. 246 taxton, עבדים and על־פני, here in the m-trad
# taxton (so this span does NOT close on silluq + sof pasuq at עבדים).
# Coordinates come from py/accgram/gen_highlight_picker.py (drag boxes over the words, export
# the `px` boxes). Note this scan is a different size again (972x259 vs 961x664 and 1149x327).
_P119_BOXES: tuple[mhi.Box, ...] = (
    mhi.Box(x=354, y=107, w=131, h=61),
    mhi.Box(x=718, y=163, w=134, h=68),
)
# Highlight rectangles in Simanim-Tanakh-p-350 pixel space (970x138, the scan's own
# resolution = the overlay viewBox). Mirroring the p. 83 / p. 246 / p. 119 highlights above,
# these two mark the same two signal words, עבדים and על־פני, here in the m-trad elyon of the
# Torah-section appendix. Coordinates come from
# py/accgram/gen_highlight_picker.py (drag boxes over the words, export the `px` boxes). Note
# this scan is a different size again (970x138 vs 961x664, 1149x327, and 972x259).
_P350_BOXES: tuple[mhi.Box, ...] = (
    mhi.Box(x=5, y=6, w=132, h=60),
    mhi.Box(x=348, y=64, w=128, h=66),
)
# Simanim *Tanakh*, a different edition from the Tiqqun though Feldheim publishes both (issue wlc-utils#62
# scope note): both its Exodus Decalogue strands are m-trad, unlike the Tiqqun's p-trad -- the
# main-Decalogue taxton (p. 119) and the elyon in the Torah section's appendix (p. 350).
_TANAKH_EX_TAHTON_IMG = "img/Simanim-Tanakh-p-119-Ex-Dec-start-m-trad-taxton.png"
_TANAKH_EX_ELYON_IMG = "img/Simanim-Tanakh-p-350-Ex-Dec-elyon-m-trad.png"
# The Deuteronomy (Vaetxanan) appendix taxton Decalogue's Shabbat commandment (p. 247): the one
# place Simanim's Tiqqun follows the m-trad, not the p-trad (the conclusion's Shabbat scope note;
# the Koren page documents the mirror-image p-trad choice at this same commandment, issue wlc-utils#66). A
# grayscale, reduced-resolution crop of the pointed (taxton) column, cropped to just the stretch
# the two traditions accent differently.
_P247_DT_IMG = "img/Simanim-Tiqqun-p-247-Deut-Dec-m-trad-taxton-Shabbat.png"
# Highlight rectangles in the p. 247 crop's pixel space (1474x383, the crop's own resolution = the
# overlay viewBox). Each Box marks one of three maqaf-compound signal words -- disjunctively
# accented chanted words that make a handy shorthand for telling the two traditions apart (they
# are not the only chanted words the traditions accent differently). Each is the disjunctively
# accented chanted word ending a row of the companion page's Sabbath-diff table:
# kol-melakha (m-trad pazer, not the p-trad geresh), ve'avdekha-va'amatekha (m-trad telisha
# gedolah -- one on each atom of the compound -- not the p-trad revia), and vekhol-behemtekha (m-trad revia,
# not the p-trad zaqef qatan). Coordinates come from
# py/accgram/gen_highlight_picker.py (drag boxes over the words, export the `px` boxes).
_P247_BOXES: tuple[mhi.Box, ...] = (
    mhi.Box(x=12, y=13, w=400, h=122),
    mhi.Box(x=465, y=111, w=457, h=128),
    mhi.Box(x=1052, y=218, w=407, h=121),
)

# Strand names and accent romanizations are single-sourced in printed_decalogue_strands (see its
# module docstring). These thin local aliases keep the prose below unchanged after the move.
_TAHTON = pds.TAHTON
_ELYON = pds.ELYON
# Each _ROM_* accent name is pre-wrapped ONCE in <span class="romanized"> (italic), so every prose
# site below is styled without a per-site rmn() call -- issue wlc-utils#65, finding C2; the rule and its
# exclusions are documented in printed_decalogue_strands' module docstring. These are HTML nodes,
# not strings: splice them into a contents tuple, never into an f-string.
_ROM_PASHTA = rmn(pds.ROM_PASHTA)
_ROM_TIPEHA = rmn(pds.ROM_TIPEHA)
_ROM_ETNAHTA = rmn(pds.ROM_ETNAHTA)
_ROM_REVIA = rmn(pds.ROM_REVIA)
_ROM_SOF_PASUQ = rmn(pds.ROM_SOF_PASUQ)
_ROM_PASHTA_ETNAHTA = rmn(pds.ROM_PASHTA_ETNAHTA)
_ROM_TIPEHA_ETNAHTA = rmn(pds.ROM_TIPEHA_ETNAHTA)
_ROM_TIPEHA_SILLUQ = rmn(pds.ROM_TIPEHA_SILLUQ)
_ROM_SILLUQ_SOF_PASUQ = rmn(pds.ROM_SILLUQ_SOF_PASUQ)
# The Deuteronomy Shabbat-commandment m-trad accents, named in the conclusion's Shabbat scope
# note (the p-trad counterparts -- geresh / revia / zaqef qatan -- are left to the companion
# page's appendix; the Koren page names some of them in its own Deuteronomy prose). _ROM_REVIA is
# already defined above.
_ROM_PAZER = rmn(pds.ROM_PAZER)
_ROM_TELISHA_GEDOLAH = rmn(pds.ROM_TELISHA_GEDOLAH)
# Named in the Simanim Tanakh verdict table for its one divergence (issue wlc-utils#69, Result 8),
# and in the p. 298 paragraphs that say why that divergence costs the page a parse.
_ROM_QADMA = rmn(pds.ROM_QADMA)
# The other two accents of the p. 298 paragraphs: the zaqef qatan p. 298 keeps from the taxton,
# and the geresh the elyon strands pair their qadma with and p. 298 does not have.  ROM_ZAQEF_QATAN
# romanizes as a bare "zaqef" (Ben, 2026-07-29 -- see that constant), which is what the prose says.
_ROM_ZAQEF_QATAN = rmn(pds.ROM_ZAQEF_QATAN)
_ROM_GERESH = rmn(pds.ROM_GERESH)
# Named only in the conclusion's grammaticality prose (issue wlc-utils#52), for the p. 246 chanted verse
# the prose checker rejects: the munax on the joined לא of לא־תעשה makes a third conjunctive
# before the pashta, where a tevir would have allowed it.  Every taxton strand has a meteg and no
# accent on that joined לא, and every elyon strand has לא as a free chanted word with a munax --
# _pin_lo_taase_strand_facts re-derives both facts from the vendored strands.  ("Where all eight
# strands have a meteg and no accent" stood here until 2026-07-29, and the עליון half of it is
# false; item 1 of doc/review-findings-2026-07-29.md.)
_ROM_MUNAX = rmn(pds.ROM_MUNAX)
# The accent the Wikisource strand has on the free לא of לא תחמד, where the Tiqqun binds it by
# maqaf instead -- named so that difference reads as an exchange rather than a missing maqaf.
_ROM_MERKHA = rmn(pds.ROM_MERKHA)
_ROM_METEG = rmn(pds.ROM_METEG)
_ROM_TEVIR = rmn(pds.ROM_TEVIR)

# The p-trad Decalogue on Hebrew Wikisource sits in the printed-tradition (נוסח הדפוסים) section
# of the very page these four strands are vendored from -- so its base URL is single-sourced from
# the data's own provenance, and we append only the section anchor here.
# That Exodus section holds BOTH p-trad strands (תחתון and עליון), which is exactly what the
# spot-check compares against.  Wikisource forms a heading's anchor id by replacing spaces with
# underscores (parentheses kept literally); the Deuteronomy copy of this heading gets a "_2"
# suffix, so the bare (suffix-less) id is the Exodus one we want.
_WIKISOURCE_PTRAD_SECTION = "הטעם התחתון מול הטעם העליון (לפי נוסח הדפוסים)"


def _wikisource_ptrad_href(source: dict) -> str:
    base = source["provenance"]["url"]
    return f"{base}#{_WIKISOURCE_PTRAD_SECTION.replace(' ', '_')}"


# --------------------------------------------------------------------------- #
# Rendering
# --------------------------------------------------------------------------- #
# This page used to open with the companion page's whole four-strands intro paragraph, duplicated
# verbatim (issue wlc-utils#65, finding V5). It now opens with ONE sentence that cues the reiteration and
# links to the companion, which alone states the four strands in full, plus the shared
# pds.MOST_STRIKING sentence (single-sourced there, verbatim on all three pages of the trio).
# Keep it that way: a reader arriving here from the companion should be able to see at a glance
# that nothing new is being said yet.
_PARA_1 = (
    "As ",
    link("the companion page", _COMPANION_PAGE_HREF),
    " explains, each Decalogue has",
    *[" ", H.bold("four"), " strands of cantillation: the"],
    *[" ", H.bold("printed tradition"), " (p-trad)"],
    " and the",
    *[" ", H.bold("manuscript tradition"), " (m-trad)"],
    f" each have their own טעם {_TAHTON} and their own טעם {_ELYON}.",
    " " + pds.MOST_STRIKING,
)

# The continuation is this page's own second paragraph (the companion page's differs).
_PARA_2 = (
    "That page lays out those four strands and grammar-checks the p-trad; this page serves only to"
    " document to what extent Simanim's Tiqqun follows the p-trad."
    " Along the way it transcribes two of the Tiqqun's notes.",
)


def _body_scans() -> tuple[object, ...]:
    """The two body-text scans that are the finding's actual evidence (issue wlc-utils#62): the body text
    the page used to only assert -- showing them is what replaced the old apology.
    """
    return (
        mhi.scan_figure(
            _P83_BODY_IMG,
            "Simanim Tiqqun p. 83: the Exodus main Decalogue in the elyon",
            (
                "The (massive) verse that starts the Simanim Tiqqun's main Decalogue (p. 83),"
                " headed",
                *[" ", H.bdi(' "עשרת הדברות" בטעם עליון'), "."],
                " Both signal words have a",
                *[" ", _ROM_REVIA, " — the p-trad ", _ELYON, "'s pair."],
                " The highlighted מצותי is the אנכי…מצותי span's shared end, where this"
                " long verse finally closes.",
                H.line_break(),
                H.small(
                    (
                        "The horizontal bar marks a removed page break — two page-scans"
                        " joined into a single column.",
                    )
                ),
            ),
            img_class="ink-on-white",
            width=None,
            boxes=_P83_BOXES,
            viewbox=(961, 664),
        ),
        mhi.scan_figure(
            _P246_BODY_IMG,
            "Simanim Tiqqun p. 246: the Exodus appendix Decalogue in the taḥton",
            (
                "The (short) two verses that start the Simanim Tiqqun's appendix Decalogue (p. 246), headed עשרת הדברות דיתרו בלא טעם עליון."
                " (Heading not shown in this image though.)"
                " Both signal words close chanted verses, each with a",
                *[" ", _ROM_SILLUQ_SOF_PASUQ, f" — the p-trad {_TAHTON}'s pair."],
                " The asterisk is a callout to the footnote transcribed below.",
            ),
            img_class="ink-on-white",
            width=None,
            boxes=_P246_BOXES,
            viewbox=(1149, 327),
        ),
    )


def _intro(source: dict) -> tuple[object, ...]:
    return (
        H.heading_level_1(REPORT_TITLE),
        H.para(_PARA_1),
        H.para(_PARA_2),
        H.para(
            (
                "Simanim's Tiqqun follows the p-trad's chanted verse boundaries for the"
                " Decalogues, though not every detail of its cantillation — the one departure,"
                " at a single commandment of its Deuteronomy appendix Decalogue, is covered in ",
                link("the conclusion", "#simanim-conclusion"),
                ". In its Exodus"
                " (Yitro) Decalogue, the Tiqqun's main Decalogue (p. 83) is the p-trad"
                f" {_ELYON} and its appendix Decalogue (p. 246) is the p-trad {_TAHTON}"
                ". The comparison throughout is against ",
                link("Hebrew Wikisource's p-trad", _wikisource_ptrad_href(source)),
                ". The two scans below show enough of"
                ' the Tiqqun\'s Exodus Decalogues to "diagnose" them both as p-trad by their'
                " signal words.",
            )
        ),
        *_body_scans(),
    )


# The figure helper is mhi.scan_figure. Every image on this page is a printed-book scan (SimTiq,
# SimTan) -- black ink, white paper -- so every call passes img_class="ink-on-white", the class
# that opts a scan into the stylesheet's dark-mode inversion. scan_figure requires that class by
# name rather than defaulting it, so the manuscript photos elsewhere in the tree (ink on
# parchment, which must NOT invert) cannot pick it up silently.


def _lines_with_breaks(lines: tuple[str, ...]) -> tuple[object, ...]:
    """Interleave ``<br>`` between transcription lines (they follow the scan's own breaks)."""
    body: list[object] = []
    for i, line in enumerate(lines):
        if i:
            body.append(H.line_break())
        body.append(line)
    return tuple(body)


# The p. 83 transcription, following the scan's own line breaks (the pointed example verse
# אנכי…עבדים is hand-set Hebrew, checked against the committed scan).
_P83_LINES = (
    "[ב] פסוק ראשון נהגו",
    "לקרותו כשמסיים",
    "ברביע כמובא בפנים,",
    "יש ספרים שנקרא כמו",
    "בטעם תחתון, כיון שע״פ",
    "המסורה צ״ל כאן יו׳ד",
    "דברות, כך: אָֽנֹכִ֖י יְהֹוָ֣ה",
    "אֱלֹהֶ֑יךָ אֲשֶׁ֧ר הֽוֹצֵאתִ֛יךָ",
    "מֵאֶ֥רֶץ מִצְרַ֖יִם מִבֵּ֥ית",
    "עֲבָדִֽים׃ [עשרת הדברות",
    "בלא טעם עליון בסוף",
    "החומש].",
)


# The standalone-verse (ten-commandment) cantillation the p. 83 note gives after "כך:" -- the same
# pointed אנכי…עבדים of _P83_LINES above, run together as one verse (silluq + sof pasuq at עבדים),
# quoted in the translation below so it shows the real text rather than describing it.
_P83_STANDALONE_VERSE = (
    "אָֽנֹכִ֖י יְהֹוָ֣ה אֱלֹהֶ֑יךָ אֲשֶׁ֧ר הֽוֹצֵאתִ֛יךָ"
    " מֵאֶ֥רֶץ מִצְרַ֖יִם מִבֵּ֥ית עֲבָדִֽים׃"
)


def _p83_scan_and_transcription() -> object:
    """Scan and transcription side by side, as in the original wlc-utils#56 comment: a two-column
    table with the source scan on the left and the RTL transcription (following the scan's own
    line breaks) on the right."""
    # As in _figure: no inline style, since gh-pages/wlc/style.css's `img { max-width: 100% }` already
    # covers it (issue wlc-utils#65, finding C4b). This img sits in a table cell rather than a <figure>, so
    # it never picked up `figure img { height: auto }` -- but height:auto is the CSS initial value
    # for a replaced element anyway, so the inline copy bought nothing here either.
    # class="ink-on-white" as in _figure -- this scan is outside a <figure>, so it takes the
    # dark-mode inversion but not the `figure img` border the rule pre-inverts alongside it.
    img = H.img(
        {
            "src": _P83_IMG,
            "alt": "Simanim Tiqqun p. 83: side-margin note on the Exodus Decalogue's אנכי…עבדים span",
            "width": "275",
            "class": "ink-on-white",
        }
    )
    header = H.table_row_of_headers(("Source scan", "Transcription"))
    body = H.table_row(
        (
            H.table_datum(img, {"style": "vertical-align: top"}),
            H.table_datum(
                _lines_with_breaks(_P83_LINES),
                {"style": "vertical-align: top", "dir": "rtl", "lang": "hbo"},
            ),
        )
    )
    return H.table((header, body), {"class": "simanim-scan-transcription"})


def _p83_section() -> tuple[object, ...]:
    return (
        H.heading_level_2(
            "Margin note on the main (עליון) Decalogue — Simanim Tiqqun p. 83"
        ),
        H.para(
            (
                "A note in the side margin of the Exodus (Yitro) Decalogue, on אנכי…עבדים.",
            )
        ),
        _p83_scan_and_transcription(),
        H.heading_level_3("Translation"),
        H.blockquote(
            (
                H.bold("[{Verse 20:}2]"),
                " {Regarding} the first {pseudo-?} verse — it is the custom of some to chant it as "
                "ending on a ",
                _ROM_REVIA,
                ", as given in the body; {but} there are editions that call for it"
                " to be chanted as in the ",
                _TAHTON,
                " since by the Masorah there must be Ten Commandments here — thus:",
                H.line_break(),
                hbo(_P83_STANDALONE_VERSE),
                H.line_break(),
                "[The Ten Commandments without the ",
                f"{_ELYON} cantillation "
                "{can be found}"
                " at the end of the ḥumash.]",
            )
        ),
        H.para(
            (
                H.small(
                    (
                        H.bold("Notation:"),
                        " text in {curly braces} is my editorial addition; ",
                        "[square brackets] reproduce square brackets present in the source itself.",
                    )
                ),
            )
        ),
        H.para(
            (
                "The note is worth reading for what it reveals about the Simanim Tiqqun's own"
                " stance: its default"
                f" {_ELYON} ends the אנכי…עבדים span on a ",
                _ROM_REVIA,
                " — the nine-verse p-trad structure — and it files the standalone,"
                " ten-verse cantillation (",
                _ROM_SILLUQ_SOF_PASUQ,
                " at עבדים) under what merely “some books” do. So the Tiqqun treats the p-trad"
                " structure as the norm and the m-trad alternative as the deviation — aware of the"
                " alternative, but not adopting it. ",
                link("Koren's note on its appendix Decalogue", _KOREN_PAGE),
                " is the mirror of this one, flagging the same alternative on the authority of"
                " רוו״ה and likewise declining to print it.",
            )
        ),
    )


# The merged (Keter / m-trad תחתון) cantillation the p. 246 note gives after "כך:" -- אנכי…עבדים
# run together as one verse, closing mid-verse rather than on a sof pasuq, quoted both in the
# transcription below and, factored out, in the translation so each shows the real text.
_P246_MERGED_VERSE = (
    "אָֽנֹכִי֙ יְהֹוָ֣ה אֱלֹהֶ֔יךָ אֲשֶׁ֧ר הֽוֹצֵאתִ֛יךָ"
    " מֵאֶ֥רֶץ מִצְרַ֖יִם מִבֵּ֣ית עֲבָדִ֑ים"
)


# The lemma the p. 246 footnote is keyed to -- its opening words, set off in the source's own
# emphasis (rendered blue here; the asterisk keys the footnote, and יי is the note's double-yod
# Tetragrammaton). Shared by the transcription and the translation so both show the same pointed,
# blue lemma.
_P246_LEMMA = "אָֽנֹכִ֖י* יְיָ֣ אֱלֹהֶ֑יךָ"

# The ordinary (רגיל / p-trad תחתון) sof-pasuq form of עבדים as the p. 246 note points it, shared
# by the transcription and the translation.
_P246_AVADIM_RAGIL = "עֲבָדִים"


def _p246_transcription() -> object:
    body = (
        f" וגו׳ כך היא הגרסה בטעם רגיל שפותח בטפחה אתנחתא ומסיים תיבת בסו״פ {_P246_AVADIM_RAGIL}: "
        f"ובכתר אר״ץ פותח בפשטא ומסיים באתנחתא, כך: {_P246_MERGED_VERSE}. ולגבי "
        '"עשרת הדברות"'
        " בטעם עליון בתוך החומש:"
    )
    return H.blockquote(
        (
            H.span_c(_P246_LEMMA, "simanim-lemma"),
            body,
        ),
        {"dir": "rtl", "lang": "hbo"},
    )


def _p246_mapping_table() -> object:
    # עבדים…אנכי columns in Hebrew reading order (right-to-left): עבדים sits left of אנכי.
    # The last column links each label to the four-strands table on the companion page.
    header = H.table_row_of_headers(
        ("the note's label", "עבדים", "אנכי", "= strand (companion page)")
    )
    ragil = H.table_row(
        (
            H.table_header(("בטעם רגיל", " ", H.small("(ordinary)"))),
            # This strand gives אנכי…עבדים its own chanted verse (pds.STRUCTURE pins that
            # verse's end at עבדים), so עבדים IS verse-final here and its U+05BD really is
            # silluq, not a meteg. Name the accent and the punctuation both, as the rest of
            # the page-set does -- "sof pasuq" alone named neither the accent nor the strand.
            H.table_datum(_ROM_SILLUQ_SOF_PASUQ),
            H.table_datum(_ROM_TIPEHA),
            # "through עבדים": the two strands are identical at every chanted word only as far as עבדים.
            # They part at the span's other signal word, על־פני, where the p-trad תחתון ends
            # another chanted verse and the m-trad עליון runs on -- which is why the companion
            # page's table gives each its own row. Don't drop the qualifier.
            H.table_datum(
                link(
                    ("p-trad ", _TAHTON, " = m-trad ", _ELYON, ", through עבדים"),
                    _FOUR_STRANDS_HREF,
                )
            ),
        )
    )
    keter = H.table_row(
        (
            H.table_header("כתר אר״ץ"),
            H.table_datum(_ROM_ETNAHTA),
            H.table_datum(_ROM_PASHTA),
            H.table_datum(link(("m-trad ", _TAHTON), _FOUR_STRANDS_HREF)),
        )
    )
    # Its own class, not the companion page's "printed-decalogue-verdict": this table maps the
    # note's labels onto strands, it renders no grammaticality verdict, and it never used that
    # class's td.clean / td.ungrammatical rules (issue wlc-utils#65, finding C4d).
    return H.table(
        (header, ragil, keter), {"class": "printed-decalogue-strand-mapping"}
    )


def _p246_section() -> tuple[object, ...]:
    return (
        H.heading_level_2(
            "Footnote on the appendix (תחתון) Decalogue — Simanim Tiqqun p. 246",
            {"id": "simanim-p246-note"},
        ),
        H.para(
            (
                f"The mirror footnote, from the appendix's {_TAHTON} Decalogue (which the"
                f" Simanim Tiqqun heads only negatively, בלא טעם עליון — lacking the {_ELYON}), on"
                " the lemma"
                " אנכי.",
            )
        ),
        mhi.scan_figure(
            _P246_IMG,
            "Simanim Tiqqun p. 246: appendix footnote on the taḥton Decalogue's אנכי…עבדים span",
            # The blue vertical bars are deliberately a different colour AND orientation from
            # the brown horizontal page-break bar (see the p. 83 elyon figure above): the two
            # mark opposite operations — a horizontal brown bar marks a page break we *removed*
            # (two scans joined), whereas these mark line breaks we *added* to a single wide
            # line. That contrast is the reason for the distinct styling, but it's mechanical
            # detail; the caption states only what each bar means, not why they look different.
            (
                "Simanim Tiqqun, p. 246 — appendix footnote contrasting בטעם רגיל and כתר אר״ץ.",
                H.line_break(),
                H.small(
                    (
                        "The vertical bars mark line breaks I added — after אתנחתא and after"
                        " עבדים — to narrow the inconveniently wide original.",
                    )
                ),
            ),
            img_class="ink-on-white",
            width=None,
        ),
        H.heading_level_3("Transcription"),
        _p246_transcription(),
        H.para(
            (
                H.small(
                    (
                        "The lemma is shown in blue in our transcription rather than boldface as"
                        " in the original.",
                    )
                ),
            )
        ),
        H.para(
            (
                H.small(
                    (
                        "It isn't clear whether the mark after עבדים in the transcription is a ",
                        _ROM_SOF_PASUQ,
                        " or a colon; I read it as a colon.",
                    )
                ),
            )
        ),
        H.heading_level_3("Translation"),
        H.blockquote(
            (
                H.span_c(hbo(_P246_LEMMA), "simanim-lemma"),
                " Such is the version in the ordinary cantillation, which"
                " opens with ",
                _ROM_TIPEHA_ETNAHTA,
                " and ends with the ",
                _ROM_SOF_PASUQ,
                " word ",
                hbo(_P246_AVADIM_RAGIL),
                "; but in the Keter Aram Tsova it opens with ",
                _ROM_PASHTA,
                " and ends with ",
                _ROM_ETNAHTA,
                ", thus: ",
                hbo(_P246_MERGED_VERSE),
                ". And as regards the “Ten" " Commandments” in the ",
                f"{_ELYON} within the ḥumash: " "{see the main part of the ḥumash?}",
            )
        ),
        H.para(
            (
                H.small(
                    (
                        "On the Simanim Tiqqun's citing the כתר אר״ץ (Aleppo Codex) here — what that citation"
                        " can and cannot mean — see ",
                        link("the note below", "#simanim-aleppo-codex"),
                        ".",
                    )
                ),
            )
        ),
        H.heading_level_3("How it maps onto the four strands"),
        H.para(
            (
                "The note contrasts two cantillations of the אנכי…עבדים span, both in the ",
                link("four-strands table on the companion page", _FOUR_STRANDS_HREF),
                ":",
            )
        ),
        _p246_mapping_table(),
        H.para(
            (
                f"So the note has the Simanim Tiqqun, in its own editorial voice, distinguishing two"
                f" {_TAHTON} cantillations of the אנכי…עבדים span: what it prints and calls the"
                f" “ordinary” (רגיל) {_TAHTON} — עבדים with ",
                _ROM_SILLUQ_SOF_PASUQ,
                f", אנכי…עבדים as its own verse, its marks identical through עבדים to the m-trad"
                f" {_ELYON} —"
                " versus the Keter's ",
                _ROM_PASHTA_ETNAHTA,
                f", the genuine m-trad {_TAHTON}, which it sets aside. The Tiqqun thus knows the two"
                " differ and knowingly prints the newer one — another glimpse of the same"
                " self-awareness as the p. 83 margin note.",
            )
        ),
    )


# --------------------------------------------------------------------------- #
# The per-Decalogue verdict tables (issue wlc-utils#69)
# --------------------------------------------------------------------------- #
# One row per Decalogue, never one per edition: p. 247's Shabbat departure and pp. 208-209's exact
# agreement cannot share a sentence, which is what killed the older per-edition wording. Each
# verdict says how far the Decalogue follows the Wikisource strand it was diffed against -- the
# claim the signal words alone cannot reach.
#
# The class turns OFF the shared odd-row zebra, as its three sibling printed-Decalogue tables do
# (issue wlc-utils#65, finding C3): the four rows alternate main / appendix, so the stripe would tint
# exactly the two appendix rows and read as if it ENCODED that rather than merely counting rows.
#
# The last column (issue wlc-utils#52) is the grammaticality verdict, and it is NOT written out per row:
# each cell is derived from the checker's own result for that transcription, looked up by the
# stem each row names, so the column cannot claim a verdict the checker does not give. The prose
# is shared with the Koren page's table -- see transcription_verdict_column.
def _verdict_table(
    rows: tuple[tuple[str, str, str, object, object], ...],
    verdicts: dict[str, tp.TranscriptionResult],
) -> object:
    header = H.table_row_of_headers(
        ("Decalogue", "pages", "strand", "how far it follows it", tvc.HEADER)
    )
    body = [
        H.table_row(
            (
                H.table_header(which),
                H.table_datum(pages),
                H.table_datum(strand),
                H.table_datum(verdict),
                H.table_datum(tvc.cell(verdicts[stem])),
            )
        )
        for which, stem, pages, strand, verdict in rows
    ]
    return H.table(
        (header, *body), {"class": "printed-decalogue-transcription-verdict"}
    )


def _tiqqun_verdict_table(verdicts: dict[str, tp.TranscriptionResult]) -> object:
    return _verdict_table(
        (
            (
                "Exodus main",
                "simtiq_ex_elyon",
                "83–84",
                ("p-trad ", _ELYON),
                (
                    "Every chanted verse boundary, the whole disjunctive skeleton, and every"
                    " chanted word marked as its Wikisource strand marks it but two, each an"
                    " exchange at the last rung. At ובנך the Wikisource strand has a maqaf where"
                    " the Tiqqun has a ",
                    _ROM_MUNAX,
                    ", separating what the Wikisource strand's maqaf makes one chanted word; at"
                    " the לא of לא תחמד the Wikisource strand has a ",
                    _ROM_MERKHA,
                    " where the Tiqqun has a maqaf, binding what that strand leaves free.",
                ),
            ),
            (
                "Exodus appendix",
                "simtiq_ex_taxton",
                "246",
                ("p-trad ", _TAHTON),
                # Not "every accent": two of its three differences are accents it adds, which is
                # what puts this row a rung above pp. 83-84's maqaf-only pair. The third is the
                # same maqaf as pp. 83-84's, named as such so this row and the scale above it stay
                # consistent (2026-07-25 claim audit, finding 3).
                (
                    "Every chanted verse boundary and the whole disjunctive skeleton, but not"
                    " every accent: three differences, none of them in a disjunctive. Two are"
                    " conjunctive accents it adds; the third is the same exchange as the Exodus"
                    " main Decalogue's, the לא of לא תחמד bound here by maqaf where its"
                    " Wikisource strand has a ",
                    _ROM_MERKHA,
                    ".",
                ),
            ),
            (
                "Deuteronomy main",
                "simtiq_dt_elyon",
                "208–209",
                ("p-trad ", _ELYON),
                "Every accent, with no difference anywhere the comparison reaches — 164 accents"
                " against 164.",
            ),
            (
                "Deuteronomy appendix",
                "simtiq_dt_taxton",
                "247",
                ("p-trad ", _TAHTON),
                (
                    "p-trad throughout ",
                    H.bold("except the Shabbat commandment"),
                    ", whose accents are m-trad — and with them the m-trad's maqaf there, or"
                    " rather its absence: לא and תעשה stand apart where the p-trad binds them."
                    " The chanted verse division stays p-trad — thirteen chanted verses, not the"
                    " m-trad's twelve — so not one verse boundary moves.",
                ),
            ),
        ),
        verdicts,
    )


def _tanakh_verdict_table(
    verdicts: dict[str, tp.TranscriptionResult], vayom_forms: tuple[str, str]
) -> object:
    strand_pair, page_pair = vayom_forms
    return _verdict_table(
        (
            (
                "Exodus main",
                "simtan_ex_taxton",
                "119–120",
                ("m-trad ", _TAHTON),
                "Every accent, with no difference anywhere the comparison reaches. Its twelve"
                " chanted verses are"
                " corroborated independently of any mark, by the edition's own printed verse"
                " numbers.",
            ),
            (
                "Deuteronomy main",
                "simtan_dt_taxton",
                "297–298",
                ("m-trad ", _TAHTON),
                (
                    "Every accent but one: a ",
                    _ROM_QADMA,
                    " on ויום where every ",
                    _TAHTON,
                    " strand has a ",
                    _ROM_PASHTA,
                    f" — all four have {strand_pair}, this page {page_pair}. It agrees with"
                    " neither ",
                    _TAHTON,
                    " strand there, so it is this edition's own departure rather than the other"
                    " tradition's, and it is the one place among these four where the departure"
                    " costs a parse: the eighth chanted verse is ungrammatical where its"
                    " Wikisource strand is clean.",
                ),
            ),
            (
                "Exodus appendix",
                "simtan_ex_elyon",
                "350",
                ("m-trad ", _ELYON),
                "Every accent, with no difference anywhere the comparison reaches.",
            ),
            (
                "Deuteronomy appendix",
                "simtan_dt_elyon",
                "351",
                ("m-trad ", _ELYON),
                "Every accent, with no difference anywhere the comparison reaches.",
            ),
        ),
        verdicts,
    )


# --------------------------------------------------------------------------- #
# The strand facts behind the p. 246 grammaticality paragraph
# --------------------------------------------------------------------------- #
# The letters the pin below finds the לא־תעשה site by -- bare letters, no marks, the marks being
# exactly what must not be retyped here (``maqaf_nonfinal_accents_page._find_span`` is this
# pattern style's fuller home).  One tuple per chanted word, so a pattern fixes the grouping as
# well as the letters; לך is in each pattern only to tell Exodus 20:4 / Deuteronomy 5:8 from the
# Sabbath commandment's לא תעשה, which כל־מלאכה follows instead.
_MAQAF = "\N{HEBREW PUNCTUATION MAQAF}"
_LO_TAASE_TAXTON = (("לא", "תעשה"), ("לך",))
_LO_TAASE_ELYON = (("לא",), ("תעשה", "לך"))


def _atom_letters(chanted_word: str) -> tuple[str, ...]:
    return tuple(
        "".join(ch for ch in atom if is_base_letter(ch))
        for atom in chanted_word.split(_MAQAF)
    )


def _run_at(version: dict, pattern: tuple[tuple[str, ...], ...]) -> list[str]:
    """The one run of chanted words in a strand whose atom letters are ``pattern``.

    Raising on anything but one match is the point: the pattern is how the pin knows it is
    still looking at the place the prose talks about.  Matches go into a list, never a set
    (item 14 of ``doc/review-findings-2026-07-29.md``: byte-identical sites dedup away).
    """
    hits = []
    for chanted_verse in version["chanted_verses"]:
        words = chanted_verse.split()
        for start in range(len(words) - len(pattern) + 1):
            run = words[start : start + len(pattern)]
            if tuple(_atom_letters(word) for word in run) == pattern:
                hits.append(run)
    assert len(hits) == 1, (version["reading"], version["tradition"], pattern, hits)
    return hits[0]


def _lo_at(version: dict, pattern: tuple[tuple[str, ...], ...]) -> str:
    """The pointed לא of the one run of chanted words in a strand whose atoms are ``pattern``."""
    return _run_at(version, pattern)[0].split(_MAQAF)[0]


def _pin_lo_taase_strand_facts(source: dict) -> None:
    """Fail the build if the strands stop supporting the p. 246 paragraph's two quantifiers.

    The paragraph on p. 246's third chanted verse says every תחתון strand has a meteg and no
    accent on the joined לא of לא־תעשה, and every עליון strand has לא as a free chanted word
    with a munax.  Until 2026-07-29 the sentence said "all eight strands have a meteg and no
    accent", which the vendored strands refute: the four עליון strands have no joined לא there
    at all (item 1 of ``doc/review-findings-2026-07-29.md``).  Both quantifiers are re-derived
    here from ``in/accgram/printed_decalogue_teamim.json`` at build time, raising rather than
    warning, like ``maqaf_nonfinal_accents_page.pin_claims`` and for the same reason: a warning
    in a generator's output is a warning nobody reads.
    """
    by_reading: dict[str, list[dict]] = {"taxton": [], "elyon": []}
    for version in source["versions"]:
        by_reading[version["reading"]].append(version)
    assert {k: len(v) for k, v in by_reading.items()} == {"taxton": 4, "elyon": 4}
    for version in by_reading["taxton"]:
        joined_lo = _lo_at(version, _LO_TAASE_TAXTON)
        accents = [ch for ch in joined_lo if is_accent(ch)]
        assert am.METEG in joined_lo and not accents, (version["section"], joined_lo)
    for version in by_reading["elyon"]:
        free_lo = _lo_at(version, _LO_TAASE_ELYON)
        accents = [ch for ch in free_lo if is_accent(ch)]
        assert accents == [am.MUNAX], (version["section"], free_lo)


# --------------------------------------------------------------------------- #
# The strand facts behind the p. 298 grammaticality paragraph
# --------------------------------------------------------------------------- #
# The two chanted words p. 298's one divergence falls on, found by their bare letters for the
# same reason the לא־תעשה patterns above are: the marks are what must not be retyped.  One tuple
# per chanted word, which also fixes the grouping -- these two are never joined by a maqaf, and
# that is the whole point of the paragraph, so a pattern that could match a compound would be
# assuming what it displays.
_VAYOM_HASHEVII = (("ויום",), ("השביעי",))


def _vayom_forms(source: dict) -> tuple[str, str]:
    """The two pairs the p. 298 paragraph shows: the תחתון strands' ויום השביעי, and p. 298's.

    Both are lifted from ``in/accgram/printed_decalogue_teamim.json`` and rendered through
    ``accents_and_letters``, which drops the vowels; a hand-typed accent would be a claim with no
    oracle behind it.  p. 298 has no pointed Hebrew of its own -- its transcription is a token
    per printed accent -- so its pair is assembled from the two strands that supply its two
    marks: the ויום of an עליון strand, which has the qadma, beside the השביעי of a תחתון strand,
    which has the zaqef qatan.  That assembly IS the finding the row states, that p. 298 has one
    עליון accent inside an otherwise תחתון-conforming Decalogue, so the asserts below check every
    strand rather than the two the forms come from.
    """
    taxton = [v for v in source["versions"] if v["reading"] == "taxton"]
    elyon = [v for v in source["versions"] if v["reading"] == "elyon"]
    assert (len(taxton), len(elyon)) == (4, 4)
    taxton_runs = [_run_at(version, _VAYOM_HASHEVII) for version in taxton]
    elyon_runs = [_run_at(version, _VAYOM_HASHEVII) for version in elyon]
    for vayom, hashevii in taxton_runs:
        assert [ch for ch in vayom if is_accent(ch)] == [am.PASHTA], vayom
        assert [ch for ch in hashevii if is_accent(ch)] == [am.ZAQEF_QATAN], hashevii
    for vayom, _ in elyon_runs:
        assert [ch for ch in vayom if is_accent(ch)] == [am.QADMA], vayom
    # "the תחתון strands'" is a claim about all four, so the rendered forms must agree across
    # them before one of them is shown as theirs; likewise the four עליון ויום.
    rendered_taxton = {
        " ".join(accents_and_letters(word) for word in run) for run in taxton_runs
    }
    rendered_elyon_vayom = {accents_and_letters(run[0]) for run in elyon_runs}
    assert len(rendered_taxton) == 1, rendered_taxton
    assert len(rendered_elyon_vayom) == 1, rendered_elyon_vayom
    strand_pair = rendered_taxton.pop()
    page_pair = (
        rendered_elyon_vayom.pop() + " " + accents_and_letters(taxton_runs[0][1])
    )
    return strand_pair, page_pair


def _conclusion(
    source: dict, verdicts: dict[str, tp.TranscriptionResult]
) -> tuple[object, ...]:
    _pin_lo_taase_strand_facts(source)
    vayom_forms = _vayom_forms(source)
    strand_pair, page_pair = vayom_forms
    return (
        H.heading_level_2("Conclusion", {"id": "simanim-conclusion"}),
        H.para(
            (
                "Simanim's Tiqqun follows the p-trad for the Decalogues, not the m-trad — fully"
                " as to chanted verse boundaries, though (per the first scope note below) not in"
                " every cantillation detail. The two"
                " traditions' most consequential divergence is over the opening span"
                " אנכי…מצותי — within each strand, a divergence of chanted verse boundaries,"
                " which can be read off the accents on the span's two signal words, עבדים and"
                " על־פני: where a signal word has a ",
                _ROM_SILLUQ_SOF_PASUQ,
                " that strand ends a chanted verse there, and where it has an ",
                _ROM_ETNAHTA,
                " or a ",
                _ROM_REVIA,
                " it runs on. The Simanim Tiqqun lands"
                f" on the p-trad side of that divergence on both strands: the p-trad {_ELYON} in"
                " its Exodus",
                f" main Decalogue (p. 83), and the p-trad {_TAHTON} in its appendix Decalogue"
                " (p. 246).",
            )
        ),
        # The transcription verdicts (issue wlc-utils#69). This is what the signal words alone could not
        # reach: they place a Decalogue among the four strands, and only an accent-by-accent
        # comparison says how far it then follows the Wikisource strand it was placed in.
        H.para(
            (
                "How far each of the four Decalogues follows that strand is a separate question"
                " from which strand it is, and one the signal words cannot answer. The verdicts"
                " are per Decalogue, since they differ. The"
                " last column adds the question ",
                link("the companion page", _COMPANION_PAGE_HREF),
                " asks of the four idealized strands, asked here of what this book actually"
                " has: run through the same prose grammar checker, does it parse?",
            )
        ),
        # Single-sourced in pds and stated verbatim on all three pages of the trio (2026-07-25 claim
        # audit, finding 3), since both verdict tables below are written in its terms: pp. 83-84
        # follow their Wikisource strand in every accent and part from it at two maqafs, and the
        # reader needs the scale to see that as one graded verdict rather than two claims at odds.
        # Splice the constant; don't paraphrase it, and don't scope it to one of the two tables.
        H.para((pds.MAQAF_IS_THE_LAST_RUNG,)),
        _tiqqun_verdict_table(verdicts),
        # The grammaticality column's two findings on this page (issue wlc-utils#52). The four p-trad
        # elyon Decalogues across this page and the Koren page print their Wikisource strand's
        # ungrammatical merged opening verse, and p. 246 departs from its Wikisource strand. Both
        # paragraphs below have to
        # keep the middle column's claim standing while adding the last column's: an intact
        # disjunctive skeleton is a token-identity fact and entails nothing about parsing.
        # GUARDRAIL (2026-07-25 claim audit, finding 5). "the only chanted verse in any of the four
        # strands that the checker rejects" left its scope to be guessed. Read per Decalogue -- the
        # four strands ARE a Decalogue's four, which is this page's frame -- it is true: exactly one
        # rejected verse among the four. Read across both books, as the rest of this very paragraph
        # is ("in both of them", two page ranges), it is false: the payload holds TWO such verses,
        # the p-trad elyon opening verse of each Decalogue. Naming the scope is the whole fix; don't
        # drop it back to a bare "the only chanted verse".
        H.para(
            (
                "Two of the four follow the p-trad ",
                _ELYON,
                ", whose opening chanted verse merges the first two commandments — the only chanted"
                " verse the checker rejects in any of a Decalogue's four strands, in Exodus and"
                " Deuteronomy alike. Simanim's"
                " Tiqqun has that verse in both of them, so pp. 83–84 and pp. 208–209 are"
                " ungrammatical there exactly as their Wikisource strand is: the ",
                link("companion page's finding", _COMPANION_PAGE_HREF),
                " in a book, rather than in an idealization of one.",
            )
        ),
        # GUARDRAIL (item 1 of doc/review-findings-2026-07-29.md). "Where all eight strands have
        # a meteg and no accent" stood in this paragraph until 2026-07-29, and the vendored
        # strands refute it: only the four תחתון strands have that. The four עליון strands have
        # לא as a free chanted word with a munax -- the very mark p. 246 has on its joined לא.
        # Both quantifiers below are re-derived from the vendored strands by
        # _pin_lo_taase_strand_facts, which raises on drift.
        H.para(
            (
                "p. 246 is the only Decalogue here whose verdict is its own rather than its"
                " Wikisource strand's, and its last two columns have to be read together. Not one of its"
                " three differences reaches a disjunctive — two are conjunctives and the third a"
                " maqaf — so the disjunctive skeleton it is credited"
                " with really is intact, and its third chanted verse, the one"
                " beginning לא־תעשה, is ungrammatical all the same, where the p-trad ",
                _TAHTON,
                " is grammatical. The page has accents on ",
                H.bold("both"),
                " atoms of that לא־תעשה, a ",
                _ROM_MUNAX,
                " on the joined לא beside the ",
                _ROM_QADMA,
                f" on תעשה. Every {_TAHTON} strand has a ",
                _ROM_METEG,
                f" and no accent on that joined לא; every {_ELYON} strand has לא as a free"
                " chanted word, with a ",
                _ROM_MUNAX,
                " of its own. The extra ",
                _ROM_MUNAX,
                " makes three conjunctives before the ",
                _ROM_PASHTA,
                " where the grammar takes two, and the checker cannot build the phrase they"
                " belong to. Take that one ",
                _ROM_MUNAX,
                " away and what is left is the Wikisource strand's accents, which parse. So"
                " an intact"
                " disjunctive skeleton does not carry a parse with it, and this is the Decalogue"
                " that shows it.",
            )
        ),
        H.para(
            (
                "What is ungrammatical is not the extra accent as such: the same ",
                _ROM_MUNAX,
                " one chanted verse earlier, on the joined לא of לא־יהיה, costs nothing, because"
                " the conjunctives there run into a ",
                _ROM_TEVIR,
                ", which allows the longer chain. The position, not the mark, is what the"
                " grammar rejects.",
            )
        ),
        # The p. 247 crop below -- a reduced-resolution, grayscale crop of the pointed taxton
        # column -- is the evidence for this scope note's Shabbat caveat: it shows the m-trad
        # accents on the three signal words _P247_BOXES highlights (see its comment).
        # (This crop was once committed but deliberately unlinked "private evidence"; issue wlc-utils#66 --
        # the Koren page's mirror finding at this same commandment -- is why it now earns a place.)
        H.para(
            (
                "One scope note: the finding above rests on the אנכי…מצותי span — the most striking"
                " p-trad/m-trad divergence. The Simanim Tiqqun makes the same p-trad choice at that"
                " span in"
                " both of its Decalogues: the Exodus (Yitro) one and the",
                f" Deuteronomy (Vaetḥanan) one, whose {_ELYON} main Decalogue starts on p. 208."
                " One caveat: in the"
                f" Deuteronomy {_TAHTON}, the p-trad and m-trad also diverge at"
                " the Shabbat commandment, but there the Tiqqun (appendix, p. 247) follows the"
                " m-trad, not the p-trad."
                " That divergence, though, moves no chanted verse boundary: the two traditions"
                " divide the Shabbat commandment into chanted verses identically, differing only"
                " on some mid-verse accents and, at לא תעשה, on a maqaf. So the precise"
                " extent of the Tiqqun's p-trad allegiance is as"
                " the title states it: the Tiqqun follows the p-trad's chanted verse boundaries"
                " without exception, but not its every cantillation detail. The scan below is"
                " that commandment, with "
                # Single-sourced in pds and shared with the Koren page's matching scope note; the
                # complementary-jobs doctrine (why this trio is not made redundant by the span's
                # own signal words, עבדים and על־פני) is spelled out at that constant.
                + pds.SHABBAT_SIGNAL_SHORTHAND
                + " — doing for accents what עבדים and על־פני do for chanted verse boundaries."
                " In the m-trad, the signal words have, respectively, a ",
                _ROM_PAZER,
                ", a ",
                _ROM_TELISHA_GEDOLAH,
                ", and a ",
                _ROM_REVIA,
                "; the ",
                link("companion page's appendix", _TAHTON_DETAILS_HREF),
                " has the full details. At this same commandment ",
                link("the Koren Tanakh", _KOREN_PAGE),
                " makes the opposite choice, keeping the p-trad accents where the Tiqqun takes"
                " the m-trad's — so the two printed-tradition editions disagree about the Shabbat"
                " commandment in opposite directions.",
            )
        ),
        mhi.scan_figure(
            _P247_DT_IMG,
            "Simanim Tiqqun p. 247: the Shabbat commandment of the Deuteronomy appendix Decalogue,"
            " in the m-trad taḥton",
            (
                "The Shabbat commandment of the Simanim Tiqqun's Deuteronomy (Vaetḥanan) appendix"
                f" Decalogue (p. 247), in the m-trad {_TAHTON} — the one place the Tiqqun departs"
                " from the p-trad. The three signal words are highlighted.",
            ),
            img_class="ink-on-white",
            width=None,
            boxes=_P247_BOXES,
            viewbox=(1474, 383),
        ),
        H.para(
            (
                "Another scope note: everything above concerns Simanim's ",
                H.bold("Tiqqun"),
                ". The separately published Simanim ",
                H.bold("Tanakh"),
                " does not agree with it: the Tanakh follows the m-trad"
                f", not the p-trad, on both strands. Where the Tiqqun is p-trad, the Tanakh's"
                f" Exodus main Decalogue (p. 119) is the m-trad {_TAHTON} and the"
                f" m-trad {_ELYON} is in the appendix to the Torah section (p. 350) — both shown"
                f" below. Its Deuteronomy Decalogue is likewise m-trad on both strands — the"
                f" {_TAHTON} in the main Decalogue (starting p. 297) and the {_ELYON} in that same"
                f" appendix, where Deuteronomy agrees with Exodus, as one would expect (neither"
                " Deuteronomy image shown). So the two Simanim editions genuinely diverge — one"
                " should not assume they agree.",
            )
        ),
        H.para(
            (
                "All four of the Tanakh's Decalogues have been transcribed accent by accent too,"
                " against their m-trad strands, so the split between the two editions is checked"
                " at the same grain as the Tiqqun's p-trad allegiance above and not merely read"
                " off the signal words. Three of the four are grammatical throughout, and none of"
                " the four meets the objection the Tiqqun's two ",
                _ELYON,
                " Decalogues do — the m-trad strands have no counterpart to the p-trad ",
                _ELYON,
                "'s merged opening chanted verse. The fourth, the Deuteronomy main Decalogue"
                " (pp. 297–298), does not parse, and its one divergence is why.",
            )
        ),
        H.para(
            (
                "That divergence is a ",
                _ROM_QADMA,
                " on ויום, where every ",
                _TAHTON,
                " strand has a ",
                _ROM_PASHTA,
                f": all four have {strand_pair}, and p. 298 has {page_pair}. All four ",
                _ELYON,
                " strands do have a ",
                _ROM_QADMA,
                " on ויום, but they pair it with a ",
                _ROM_GERESH,
                " on השביעי, where p. 298 keeps the ",
                _TAHTON,
                "'s ",
                _ROM_ZAQEF_QATAN,
                " — so what p. 298 has is one ",
                _ELYON,
                " accent inside an otherwise ",
                _TAHTON,
                "-conforming Decalogue. A ",
                _ROM_QADMA,
                " immediately before a ",
                _ROM_ZAQEF_QATAN,
                " is a familiar pair when the two stand on one chanted word: that is the",
                " metigah of a metigah-zaqef. Here the ",
                _ROM_QADMA,
                " and the ",
                _ROM_ZAQEF_QATAN,
                " do not stand on one chanted word. ויום and השביעי are two chanted"
                " words, with a space between them and no maqaf, and both Yeivin and Breuer"
                " restrict the metigah to the chanted word of the zaqef — Yeivin's ",
                itm(),
                " §223, “the word bearing zaqef”, and Breuer's ",
                cos(),
                " ch. 5 §4, “a [metigah] will appear in the word of the [zaqef qatan]”, the"
                " bracketed names being this page's, in place of the translator's.",
            )
        ),
        H.para(
            (
                "So that ",
                _ROM_QADMA,
                " on ויום is very likely the edition's error. That is a stronger thing to say"
                " than anything said about p. 246 above, and the difference is in what the two"
                " marks are. The extra ",
                _ROM_MUNAX,
                " on p. 246 is a well-formed accent in a chain the grammar finds one too long; a"
                " tradition that chants it is not ruled out by anything here. The ",
                _ROM_QADMA,
                " on p. 298 fits no configuration either book allows, and it stands alone against"
                " all four ",
                _TAHTON,
                " strands.",
            )
        ),
        _tanakh_verdict_table(verdicts, vayom_forms),
        mhi.scan_figure(
            _TANAKH_EX_TAHTON_IMG,
            "Simanim Tanakh p. 119: the Exodus main Decalogue, in the m-trad taḥton",
            (
                "Simanim Tanakh, p. 119 — the start of the Exodus main Decalogue, in"
                f" the m-trad {_TAHTON} cantillation. The highlighted signal words are the"
                " m-trad ",
                _TAHTON,
                "'s pair: עבדים has an ",
                _ROM_ETNAHTA,
                " and על־פני a ",
                _ROM_SILLUQ_SOF_PASUQ,
                ".",
            ),
            img_class="ink-on-white",
            width=None,
            boxes=_P119_BOXES,
            viewbox=(972, 259),
        ),
        mhi.scan_figure(
            _TANAKH_EX_ELYON_IMG,
            "Simanim Tanakh p. 350: the Exodus Decalogue in the appendix to the Torah section, in the m-trad elyon",
            (
                "Simanim Tanakh, p. 350 — the Exodus Decalogue in the appendix to the Torah"
                f" section, in the m-trad {_ELYON} cantillation. The highlighted signal words"
                " are the m-trad ",
                _ELYON,
                "'s pair: עבדים has a ",
                _ROM_SILLUQ_SOF_PASUQ,
                " and על־פני a ",
                _ROM_REVIA,
                ".",
            ),
            img_class="ink-on-white",
            width=None,
            boxes=_P350_BOXES,
            viewbox=(970, 138),
        ),
        H.para(
            (
                "The two editions also swap which strand goes in the main Decalogue and which in an"
                " appendix, as one would expect from their different purposes: the Tiqqun runs the"
                f" {_ELYON} in its main Decalogue and appends the {_TAHTON}, whereas the Tanakh does"
                f" the reverse — the everyday {_TAHTON} in the main Decalogue and the {_ELYON} in an"
                " appendix. And because this is a Tanakh, not a Torah-only Tiqqun, that appendix"
                " sits at the end of the Torah section — mid-volume, before the Prophets — not at"
                " the back of the book.",
            )
        ),
    )


def _aleppo_codex_section() -> tuple[object, ...]:
    return (
        H.heading_level_2(
            "On the Simanim Tiqqun's citation of the Aleppo Codex",
            {"id": "simanim-aleppo-codex"},
        ),
        H.para(
            (
                link("The p. 246 note", "#simanim-p246-note"),
                " cites the כתר אר״ץ (Keter Aram Tsova, the Aleppo Codex) for the ",
                _ROM_PASHTA_ETNAHTA,
                " cantillation. Two things are worth keeping straight about that citation.",
            )
        ),
        H.unordered_list(
            (
                (
                    H.bold(
                        "It names one of the Codex's two Decalogue cantillations, not"
                        " “the” cantillation."
                    ),
                    " The ",
                    _ROM_PASHTA_ETNAHTA,
                    f" cantillation is the m-trad {_TAHTON} — one strand. Like the Tiberian"
                    " manuscripts generally, the Aleppo Codex's Decalogue has both"
                    f" cantillations; the {_ELYON} is the other (אנכי…עבדים as its own verse, ",
                    _ROM_TIPEHA_SILLUQ,
                    f"). Citing the {_TAHTON} strand alone does not mean the Codex has only one.",
                ),
                (
                    H.bold("And it is a reconstruction, not an autopsy."),
                    " The Aleppo Codex's Torah survives only from Deut 28:17 onward, so the"
                    " physical Codex contains neither Decalogue; any statement about how “the"
                    " Keter” points אנכי…עבדים rests on reconstruction or pre-1947 testimony.",
                ),
            )
        ),
        H.para(
            (
                "Perhaps the editors of the Simanim Tiqqun felt there was no room for such details,"
                " but strictly speaking, they should have said something like"
                " “one of the two cantillations reconstructed for the Aleppo Codex is …”.",
            )
        ),
    )


def render_body_contents(
    source: dict, verdicts: dict[str, tp.TranscriptionResult]
) -> tuple[object, ...]:
    return (
        *_intro(source),
        *_p83_section(),
        *_p246_section(),
        *_conclusion(source, verdicts),
        *_aleppo_codex_section(),
    )


def default_html_out_path(repo_root: Path) -> Path:
    return paths.wlc_pages_dir() / "accgram" / "printed-decalogue-simanim.html"


def add_args(parser: argparse.ArgumentParser, repo_root: Path) -> None:
    parser.add_argument("--source", type=Path, default=pd.default_source_path())
    parser.add_argument(
        "--html-out", type=Path, default=default_html_out_path(repo_root)
    )


def run(args: argparse.Namespace) -> None:
    # The four-strands table lives on the companion page, so this page tabulates none of the
    # strands' own verdicts -- but it does need them, since the verdict tables' last column
    # states each transcription's verdict AGAINST its Wikisource strand's (issue wlc-utils#52). Both checks
    # together are a fraction of a second, so nothing here is worth skipping for regeneration
    # speed.
    source = pd.load_source(args.source)
    verdicts = tvc.by_stem(tp.check_all(pd.check_all(source)))

    html_out: Path = args.html_out
    html_out.parent.mkdir(parents=True, exist_ok=True)
    H.write_html_to_file(
        body_contents=render_body_contents(source, verdicts),
        write_ctx=H.WriteCtx(
            title=REPORT_TITLE,
            path=str(html_out),
            centered=True,
            html_comment=provenance.generated_html_comment(__file__),
        ),
        path_to_style=rtms_report.path_to_gh_pages_style(html_out),
    )
    print(f"HTML: {html_out}")


def main() -> None:
    force_utf8_io()
    repo_root = paths.repo_root()
    parser = argparse.ArgumentParser(description=__doc__)
    add_args(parser, repo_root=repo_root)
    run(parser.parse_args())


if __name__ == "__main__":
    main()
