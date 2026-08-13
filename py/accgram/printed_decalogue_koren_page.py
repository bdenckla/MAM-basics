r"""Generate gh-pages/wlc/accgram/printed-decalogue-koren.html -- does the Koren Tanakh follow the
printed or the manuscript Decalogue tradition?  Answer: the printed tradition.

Companion to ``printed_decalogue_simanim_page``: the same question, asked of Koren instead of
Simanim's Tiqqun.  The four cantillation strands of the opening אנכי…מצותי span are derived live
from the vendored ``in/accgram/printed_decalogue_teamim.json`` by the shared
``printed_decalogue_strands`` module and tabulated on the ``printed-decalogue`` companion page;
this page links to that table rather than duplicating it, and serves only to document Koren's
place in the p-trad camp -- plus one Koren note that shows the same editorial self-awareness the
Simanim page found in SimTiq.

What establishes the answer is Koren's *body text*: its Exodus main Decalogue (pp. 113-114) is the
p-trad תחתון and its appendix Decalogue (p. A38) the p-trad עליון, and both are compared, by
the author, against what Hebrew Wikisource records as the printed tradition, and they match.  That
body text is asserted here, not transcribed word-for-word (only shown as scans).

Since issue wlc-utils#69 the claim rests on more than a spot-check: all FOUR Koren Decalogues have a
committed hand transcription of every printed accent (``in/accgram/edition_transcriptions/
koren_*.txt``), diffed against the vendored strand and pinned by
``tests/test_edition_transcriptions.py``.  TWO of the four match their Wikisource strand mark
for mark; the other two -- both appendix ones -- differ from it only at the maqaf, the Exodus
one splitting two compounds that strand joins and the Deuteronomy one joining one it leaves
apart.  A maqaf difference is an ordinary difference at the bottom of the trio's one scale,
stated to the reader
via ``printed_decalogue_strands.MAQAF_IS_THE_LAST_RUNG``; a 2026-07-25 claim audit found this page
using "every accent" two ways at once (see the guardrail comments below), so every verdict here
names the first rung that breaks rather than claiming a bare "every accent".  ``_verdict_table``
renders the four, one row per Decalogue -- never one per edition, since the four verdicts differ.

The one *note* is the secondary, more-for-fun material -- kept for how aware Koren is of the older,
printed-tradition choice it makes:

  * **appendix p. A38** (עליון): a note on the merged עליון Decalogue, citing רוו״ה
    (= ר' וולף היידנהיים, R. Wolf Heidenheim), directing that the First Commandment -- through
    מבית עבדים -- be read בטעם התחתון, i.e. as its own chanted verse rather than merged into the
    long opening verse the עליון body prints.  This is the exact mirror of SimTiq's p. 83
    side-margin note: the עליון body ends אנכי…עבדים on a revia, and the note flags the
    standalone-verse (ten-commandment) alternative it declines to print.

The verdict table's LAST column is issue wlc-utils#52's question asked of these four: run through accgram's
prose checker, is Koren's accentuation grammatical, and as grammatical as the Wikisource strand
it follows?  All four give their Wikisource strand's verdicts exactly, which for the two
APPENDIX (עליון) Decalogues means printing the p-trad עליון's merged opening chanted verse --
the one the checker rejects.  So the
p. A38 note above happens to name the alternative the checker's objection points at: read the
First Commandment in the תחתון and the merged verse never arises.  The note argues from the count
of ten commandments and says nothing about grammar, so the conclusion states that as a coincidence
of subject and credits Koren with no grammatical motive.  The cells come live from
``transcription_verdict_column``, shared with the Simanim page so the two cannot drift.

Editorial / style conventions are shared with the two companion pages and documented on
``printed_decalogue_strands`` (bare-Hebrew strand names תחתון / עליון -- never transliterated or
translated; the single-sourced ``ROM_*`` accent romanizations; the real-em-dash rule).  The thin
``_TAHTON`` / ``_ELYON`` aliases below just limit prose churn; the ``_ROM_*`` ones additionally
wrap each name in the italic ``span.romanized``, so they are HTML nodes rather than strings (see
the comment at that alias block).  As on the Simanim
page: prefer "cantillation" to "accentuation"; keep romanized names ("taḥton") in image ``alt``
text on purpose (attribute contexts are exempt from the Hebrew-letter rule by design -- see the
"Attribute contexts are EXEMPT" bullet in ``printed_decalogue_strands``); and keep the two term
pairs strictly apart.  *main* vs *appendix* = the book's two parts (the running Torah text vs the
Decalogue reprinted in the appendix) -- use "main" ONLY for that pair, worded as "main Decalogue" /
"appendix Decalogue", never "main text"; and *body* (printed text) vs *note* (annotation).  Do not
regress "main" to "running text" here: the Simanim page's docstring is the fuller statement of this
rule.  (Note Koren is a **Tanakh**, not a ḥumash -- the Simanim page glosses this same pair as "the
running ḥumash", which is right for its Torah-only Tiqqun but would be wrong here.)

DRAFT-STAGE FACTS TO VERIFY (issue wlc-utils#70, which collects everything awaiting the physical book):
the appendix page numbers (A38 / A39) come from the committed scan filenames, as does the fact
that the page never says where the appendix physically sits; and רוו״ה is *tentatively* expanded
to Wolf Heidenheim (likely but unconfirmed, flagged as such in the rendered notation line).
The Exodus main Decalogue's extent is NO LONGER draft-stage: transcribing it settled that it runs
pp. 113-114, p. 113 breaking mid-20:12, so every prose citation reads "pp. 113-114".  (The p. 113
figure caption stays a bare "p. 113" on purpose -- it captions a scan of the Decalogue's start,
which really is on p. 113.)

Two readings on these pages were flagged uncertain during transcription and are pinned in
``_UNCERTAIN_READINGS``: p. 114's לא of לא תרצח and p. 281's tipexa on את־שמו.  Neither appears on
the rendered page in any form -- Ben's call, 2026-07-24 (issue wlc-utils#69 decision 8): both are bounded to
discriminate nothing this page claims, neither can move a verdict, their reader-facing home is
issue wlc-utils#70, and the page assumes them true.  Don't add a hedge or a footnote for them.

The appendix's separate pagination IS now confirmed (Ben, 2026-07-15), which is why every citation
of it reads "p. A38", never a bare "p. 38": the appendix restarts its own page numbering at 1, so
an unprefixed 38 would read as page 38 of the book's main part and, being lower than the main
Decalogue's own p. 113, would wrongly suggest the appendix sits *before* it.  Keep the A prefix on
appendix citations, and don't "normalize" it away.  (The scan *filenames* keep their original
``Koren-appendix-p-38-...`` spelling -- they are committed assets, and "appendix" already
disambiguates them.)

Koren's Deuteronomy (Vaetxanan) Decalogue *has* now been spot-checked (issue wlc-utils#66), so the claim is
no longer Exodus-scoped: Koren has the p-trad in both books.  The Deuteronomy check also reaches
a second divergence point the Exodus scans cannot -- the Shabbat commandment -- where Koren again
has the p-trad, and where Simanim's Tiqqun does not (an accents-only departure: Simanim's Tiqqun
still follows the p-trad's chanted verse boundaries).  See the conclusion's scope note.

Its Deuteronomy עליון is no longer unchased either.  The page long carried a sentence saying the
Deuteronomy half of the claim rested on the תחתון alone because that appendix Decalogue had never
been checked; ``koren_dt_elyon`` (p. A39) transcribes it, with zero divergences, so the sentence
was false and is gone.  Don't reinstate it.

Regenerate with ``main_accgram.py generate-html``; test with
``tests/test_printed_decalogue_koren.py`` (plus the tree-wide ``tests/test_transliterations.py``).
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from accgram import maqaf_nonfinal_accents as mpa
from accgram import printed_decalogue as pd
from accgram import printed_decalogue_strands as pds
from accgram import printed_decalogue_taxton_diff as pdt
from accgram import rtms_report
from accgram import transcription_parse as tp
from accgram import transcription_verdict_column as tvc
from accgram.almost_errors_html_shared import accents_and_letters, hbo, link
from wlc_cmn.utf8_io import force_utf8_io
from mb_cmn import paths
from mb_cmn import provenance

from py_html import my_html_for_img as mhi
from py_html import wlc_utils_html as H
from py_html.my_html_span_romanized import rmn

# Plural "Decalogues" since issue wlc-utils#66: the claim now genuinely covers Exodus and Deuteronomy both,
# so the Simanim page's plural policy (claims about both Decalogues take the plural) applies here
# too. It was singular only while the page was Exodus-scoped.
REPORT_TITLE = "Koren follows the printed tradition for the Decalogues"

_PRINTED_DECALOGUE_PAGE = "printed-decalogue.html"
_SIMANIM_PAGE = "printed-decalogue-simanim.html"
# The survey of accents on a non-final atom of a compound (issue wlc-utils#76), narrowed since 4bc2d7f
# and f9d966d to MAM's prose verses -- so it gives this page's Deuteronomy maqaf difference its
# rate, and the WLC precedent is stated and pinned HERE, by _wlc_munax_munax_compounds (item 4
# of doc/review-findings-2026-07-29.md).  Generated by accgram/maqaf_nonfinal_accents_page.py.
_MAQAF_NONFINAL_PAGE = "maqaf-nonfinal-accents.html"
# The four-strands table lives on the companion page (issue wlc-utils#52); cross-references whose link text
# names the table land on its heading anchor there rather than on a local table.
_FOUR_STRANDS_HREF = f"{_PRINTED_DECALOGUE_PAGE}#four-strands"
# Link text that names the page, not the table, gets the page itself: an anchor would drop the
# reader past the companion's own intro, mid-page, which is not what "the companion page" promises.
_COMPANION_PAGE_HREF = _PRINTED_DECALOGUE_PAGE
# The companion's appendix cataloguing how the two תחתון strands differ (its heading id there,
# _TAHTON_DETAILS_ID) -- the reference for the Shabbat-commandment accent details this page omits.
_TAHTON_DETAILS_HREF = f"{_PRINTED_DECALOGUE_PAGE}#tahton-details"
# The companion's dissection of the one chanted verse the prose checker rejects -- the merged
# opening verse of the p-trad עליון, which is what this page's two appendix Decalogues print.
_ELYON_FAILS_HREF = f"{_PRINTED_DECALOGUE_PAGE}#why-the-printed-elyon-fails"
# This page's own p. A38 note section, linked from the conclusion's grammaticality paragraph.
_PA38_NOTE_ID = "koren-pa38-note"

# Body-text scans: the two Koren Exodus Decalogues whose cantillation establishes the p-trad
# finding -- the תחתון in the main Decalogue (p. 113) and the עליון in the appendix (p. A38).
_P113_BODY_IMG = "img/Koren-p-113-Ex-Dec-p-trad-taxton.png"
_PA38_BODY_IMG = "img/Koren-appendix-p-38-Ex-Dec-p-trad-elyon.png"
# The Deuteronomy (Vaetxanan) תחתון Decalogue starts on p. 280 and runs onto p. 281; this crop is
# its Shabbat commandment, on p. 281. It backs the conclusion's scope note (issue wlc-utils#66): unlike
# Simanim's Tiqqun, Koren has the p-trad here too.
_P281_DT_BODY_IMG = "img/Koren-p-281-Dt-Dec-Shabbat-p-trad-taxton.png"
# The Koren note (a crop of the appendix p. A38 עליון Decalogue): the רוו״ה footnote transcribed and
# translated below.
_PA38_NOTE_IMG = "img/Koren-appendix-p-38-Ex-Dec-p-trad-elyon-note.png"

# Word-highlight boxes on the p. 113 taxton scan, in the scan's own pixel space (viewbox 936x262,
# the rectified grayscale image's natural size). Picked with gen_highlight_picker.py; they mark the
# boundary words of the אנכי…עבדים span the caption discusses.
_P113_BOXES: tuple[mhi.Box, ...] = (
    mhi.Box(x=466, y=112, w=138, h=59),
    mhi.Box(x=796, y=162, w=131, h=69),
)
# Word-highlight boxes on the p. 281 Deuteronomy Shabbat scan, in the scan's own pixel space
# (viewbox 913x186, its natural size). Picked with gen_highlight_picker.py; they mark the three
# signal words the conclusion's scope note names. The middle word wraps the scan's line break
# (וְעַבְדְּךָ ends one line, וַאֲמָתֶךָ starts the next), so it is boxed on its accent-bearing half.
_P281_BOXES: tuple[mhi.Box, ...] = (
    mhi.Box(x=431, y=27, w=189, h=67),
    mhi.Box(x=791, y=92, w=118, h=73),
    mhi.Box(x=389, y=89, w=190, h=70),
)
# Word-highlight boxes on the Koren appendix p. A38 elyon scan, in the scan's own pixel space
# (viewbox 850x472, its natural size). Picked with gen_highlight_picker.py; the three boxes mark,
# in text order, the אנכי…מצותי span's two signal words, עבדים and על־פני, plus מצותי -- the span's
# shared end, marked for orientation, not as a signal (every strand closes a chanted verse there,
# so it distinguishes nothing; the p-trad elyon shown here runs the whole way to it in one verse).
# על־פני wraps the scan's line break (על ends line 2, פני starts line 3), so it is boxed on its פני
# half. This is the direct analog of the Simanim Tiqqun p. 83 elyon
# (printed_decalogue_simanim_page._P83_BOXES), which marks the same three words on its own elyon
# scan (the Simanim page's other scans, being taxton or m-trad, close a verse earlier and mark
# two signal words).
_PA38_BOXES: tuple[mhi.Box, ...] = (
    mhi.Box(x=452, y=77, w=109, h=61),  # עבדים (line 2)
    mhi.Box(x=787, y=136, w=61, h=66),  # על־פני -- its פני, start of line 3
    mhi.Box(x=205, y=381, w=123, h=62),  # מצותי (last line)
)

# Strand names and accent romanizations are single-sourced in printed_decalogue_strands (see its
# module docstring). These thin local aliases keep the prose below unchanged.
_TAHTON = pds.TAHTON
_ELYON = pds.ELYON
# Each _ROM_* accent name is pre-wrapped ONCE in <span class="romanized"> (italic), so every prose
# site below is styled without a per-site rmn() call -- issue wlc-utils#65, finding C2; the rule and its
# exclusions are documented in printed_decalogue_strands' module docstring. These are HTML nodes,
# not strings: splice them into a contents tuple, never into an f-string.
_ROM_REVIA = rmn(pds.ROM_REVIA)
_ROM_SILLUQ_SOF_PASUQ = rmn(pds.ROM_SILLUQ_SOF_PASUQ)
# Koren's p-trad accents on the three Shabbat-commandment signal words (issue wlc-utils#66), named only in
# the conclusion's scope note. The m-trad counterparts (pazer / telisha gedolah / revia) are left
# to the companion page's appendix, not repeated here. _ROM_REVIA is already defined above.
_ROM_GERESH = rmn(pds.ROM_GERESH)
_ROM_ZAQEF_QATAN = rmn(pds.ROM_ZAQEF_QATAN)
# Named only in the conclusion's maqaf paragraph, for the accent לך carries where the
# תחתון strands leave it standing alone -- the reading that refutes this page's old "no strand at
# all separates יהיה from לך" (see the guardrail comment there).
_ROM_TEVIR = rmn(pds.ROM_TEVIR)
# The accent the Deuteronomy appendix Decalogue keeps on the לא it joins by maqaf: the compound is
# accented on BOTH atoms, which is why that maqaf is invisible to the token diff.
_ROM_MUNAX = rmn(pds.ROM_MUNAX)

# The p-trad Decalogue on Hebrew Wikisource sits in the printed-tradition (נוסח הדפוסים) section of
# the very page these four strands are vendored from -- so its base URL is single-sourced from the
# data's own provenance, and we append only the section anchor here. (Same rule as the Simanim
# page; see its ``_wikisource_ptrad_href``.)
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

_PARA_2 = (
    "That page lays out those four strands and grammar-checks the p-trad; this page serves only to"
    " document the claim that Koren follows the p-trad."
    " Along the way it transcribes one of Koren's notes.",
)


# The figure helper is mhi.scan_figure. Every image on this page is a Koren scan -- black ink,
# white paper -- so every call passes img_class="ink-on-white", the class that opts a scan into
# the stylesheet's dark-mode inversion. scan_figure requires that class by name rather than
# defaulting it, so the manuscript photos elsewhere in the tree (ink on parchment, which must NOT
# invert) cannot pick it up silently.


def _lines_with_breaks(lines: tuple[str, ...]) -> tuple[object, ...]:
    """Interleave ``<br>`` between transcription lines (they follow the scan's own breaks)."""
    body: list[object] = []
    for i, line in enumerate(lines):
        if i:
            body.append(H.line_break())
        body.append(line)
    return tuple(body)


def _body_scans() -> tuple[object, ...]:
    """The two body-text scans that are the finding's actual evidence -- elsewhere the page only
    asserts Koren's body text, here it is shown.  (The captions below name the strands and pages.)
    """
    return (
        mhi.scan_figure(
            _P113_BODY_IMG,
            "Koren p. 113: the Exodus main Decalogue in the p-trad taḥton",
            (
                "The start of Koren's Exodus main Decalogue (p. 113), in"
                f" the p-trad {_TAHTON}. אנכי…עבדים is its own chanted verse — the signal word"
                " עבדים closes it with a",
                *[" ", _ROM_SILLUQ_SOF_PASUQ, "."],
            ),
            img_class="ink-on-white",
            width=None,
            boxes=_P113_BOXES,
            viewbox=(936, 262),
        ),
        mhi.scan_figure(
            _PA38_BODY_IMG,
            "Koren appendix p. A38: the Exodus appendix Decalogue in the elyon",
            (
                "The start of Koren's Exodus appendix Decalogue (p. A38), in the p-trad"
                f" {_ELYON}. Both signal words have a",
                *[" ", _ROM_REVIA, " — the p-trad ", _ELYON, "'s pair."],
                " The verse runs on to the highlighted מצותי, the אנכי…מצותי span's shared end.",
            ),
            img_class="ink-on-white",
            width=None,
            boxes=_PA38_BOXES,
            viewbox=(850, 472),
        ),
    )


def _intro(source: dict) -> tuple[object, ...]:
    return (
        H.heading_level_1(REPORT_TITLE),
        H.para(_PARA_1),
        H.para(_PARA_2),
        H.para(
            (
                "Koren follows the p-trad for the Decalogues. In its Exodus"
                " Decalogue, Koren's main Decalogue (pp. 113–114) is the p-trad"
                f" {_TAHTON} and its appendix Decalogue (p. A38) is the p-trad {_ELYON}"
                ". The comparison throughout is against ",
                link("Hebrew Wikisource's p-trad", _wikisource_ptrad_href(source)),
                ". The two scans below show enough of"
                ' Koren\'s Exodus Decalogues to "diagnose" them both as p-trad.',
            )
        ),
        *_body_scans(),
    )


# The Koren note, following the scan's own two line breaks. It is unpointed prose (no cantillation),
# so unlike the SimTiq note transcriptions there is no hand-set pointed verse to check. רוו״ה carries a
# gershayim (U+05F4); the quoted lemma "מבית עבדים" reproduces the note's own straight quotes.
_PA38_NOTE_LINES = (
    'לדעת רוו״ה, יש לקרוא את הדיבר הראשון עד "מבית עבדים"',
    "בטעם התחתון.",
)


def _pa38_note_section() -> tuple[object, ...]:
    return (
        H.heading_level_2(
            "Note on the appendix (עליון) Decalogue — Koren p. A38",
            {"id": _PA38_NOTE_ID},
        ),
        H.para(
            (
                "A note on the appendix Decalogue, keyed to the opening commandment אנכי…עבדים and"
                " citing רוו״ה.",
            )
        ),
        mhi.scan_figure(
            _PA38_NOTE_IMG,
            "Koren appendix p. A38: note on the elyon Decalogue's אנכי…עבדים span",
            (
                "Koren, appendix p. A38 — the note on the",
                f" {_ELYON} Decalogue, citing רוו״ה.",
            ),
            img_class="ink-on-white",
            width=None,
        ),
        H.heading_level_3("Transcription"),
        H.blockquote(
            _lines_with_breaks(_PA38_NOTE_LINES),
            {"dir": "rtl", "lang": "hbo"},
        ),
        H.heading_level_3("Translation"),
        H.blockquote(
            (
                "In the opinion of רוו״ה {R. Wolf Heidenheim}, one should read the First"
                " Commandment (up to “מבית עבדים”) in the ",
                _TAHTON,
                ".",
            )
        ),
        H.para(
            (
                H.small(
                    (
                        H.bold("Notation:"),
                        " text in {curly braces} is my editorial addition. That includes the"
                        " expansion of the abbreviation רוו״ה, which I tentatively"
                        " read as ר' וולף היידנהיים (R. Wolf Heidenheim) — the grammarian whose"
                        " editions fixed much of the printed dual-cantillation norm, so the"
                        " likeliest referent here, though I have not confirmed the expansion."
                        " The parentheses are likewise an editorial addition; the note itself has"
                        " none.",
                    )
                ),
            )
        ),
        H.para(
            (
                "The note is the mirror of the ",
                link("Simanim Tiqqun's p. 83 side-margin note", _SIMANIM_PAGE),
                ". Koren's appendix has the ",
                _ELYON,
                " by default — the merged, nine-verse p-trad structure, in which אנכי…עבדים ends"
                " on a ",
                _ROM_REVIA,
                " rather than closing its own verse. The note flags the alternative, on רוו״ה's"
                " authority: read the First Commandment (through מבית עבדים) in the ",
                _TAHTON,
                " — i.e. as its own chanted verse (",
                _ROM_SILLUQ_SOF_PASUQ,
                " at עבדים), which keeps ten distinct commandments. That ",
                _TAHTON,
                " cantillation is one of the ",
                link("four strands on the companion page", _FOUR_STRANDS_HREF),
                " (the p-trad ",
                _TAHTON,
                ", identical on its boundary words to the m-trad ",
                _ELYON,
                " — through עבדים; at the span's other signal word, על־פני, the two part). So"
                " Koren, like the Simanim Tiqqun, prints the p-trad structure as the norm and"
                " files the standalone-verse alternative under what one authority merely"
                " recommends —"
                " aware of the alternative, but not adopting it.",
            )
        ),
    )


# --------------------------------------------------------------------------- #
# The per-Decalogue verdict table (issue wlc-utils#69)
# --------------------------------------------------------------------------- #
# One row per Decalogue, never one per edition -- the rule the Simanim page's own table follows,
# and for the same reason: how far a Decalogue follows its Wikisource strand differs between the
# four, so a single per-edition verdict would have to be either false or vacuous. The class turns
# OFF the shared odd-row zebra as its sibling printed-Decalogue tables do (issue wlc-utils#65, finding
# C3): the rows alternate main / appendix, so the stripe would tint exactly the two appendix rows
# and read as if it encoded that.
#
# The two readings flagged uncertain during transcription (p. 114's לא of לא תרצח, p. 281's tipexa
# on את־שמו) are deliberately NOT mentioned here or anywhere on this page -- Ben's call,
# 2026-07-24. Both are bounded to discriminate nothing this page claims, neither can move a
# verdict, and their reader-facing home is issue wlc-utils#70; the page assumes both readings true and
# states its verdicts flat. Don't reintroduce them as a hedge or a footnote.
#
# The last column (issue wlc-utils#52) is the grammaticality verdict, and it is NOT written out per row:
# each cell comes from the checker's own result for the transcription the row names, so the column
# cannot claim a verdict the checker does not give. Its prose is shared with the Simanim page's
# table -- see transcription_verdict_column.
#
# GUARDRAIL on the "how far it follows it" column (2026-07-25 claim audit, finding 3). Two rows
# said more than they had. The Deuteronomy appendix row claimed "Every accent, with no difference
# anywhere" although that page JOINS לא־תעשה into a maqaf compound where ws/dt/elyon/printed sets
# the two atoms apart -- token-invisible (the streams are identical with the maqaf dropped) but a
# real difference, so "no difference anywhere" was false and only "no ACCENT difference" is true.
# And the Deuteronomy main row's "five independent ways" was a count with no stated criterion,
# unreconcilable with the hub's "three" and the test suite's "eight" for the same divergence set.
# Both are fixed by the same two moves, which any rewrite must keep: scope every "no difference"
# to accents, and take the divergence-set counts from printed_decalogue_taxton_diff rather than
# typing them (``counts`` below is derived and raises on drift).
#
# THE ONE VOWEL, and why the two rows may state it (2026-07-25). The twelfth Deuteronomy site and
# the fifth Exodus one are the same chanted word and are not accent differences at all: the m-trad has
# qamats in תִרְצָ֖ח where the p-trad has patax, on the same tipexa. A transcription of accents
# cannot carry that, so until now the Deuteronomy row hedged it as "the last one of vowels alone"
# and claimed nothing about which vowel Koren has -- nobody had looked. Both were then read off
# the committed page scans, and both are patax, the p-trad vowel:
#   * Deuteronomy, A5-D-281.jpg p. 281 printed line 12 (the line the .txt gives as "silsof mer tip
#     mun", לך׃ לא תרצח ולא);
#   * Exodus, A2-E-114.jpg p. 114 printed line 1.
# The reading is decidable rather than a judgement call because this type distinguishes the two
# unmistakably and both controls sit on the same page: its qamats is a bar with a blob attached
# below the bar's centre (p. 281 line 11, the final kaf of אלהיך), its patax a bare bar (the same
# line's xataf patax under the alef of אשר). Under the tsadi of תרצח there is a bare bar plus,
# lower and to its left, the detached hook this type uses for tipexa -- the same hook that sits
# under the he of that line's own אלהיך. No blob: patax.
# This is a primary observation about the physical edition and it is NOT in the transcription
# apparatus, which by design records accents only. Its home is the note in each transcription's
# .txt comment block (the same place the pasoleg_kinds observation lives). Do not restate it as a
# fact the diff establishes, and do not expect a test to defend it.
def _verdict_table(
    verdicts: dict[str, tp.TranscriptionResult], counts: dict[str, int]
) -> object:
    header = H.table_row_of_headers(
        ("Decalogue", "pages", "strand", "how far it follows it", tvc.HEADER)
    )
    rows = (
        (
            "Exodus main",
            "koren_ex_taxton",
            "113–114",
            ("p-trad ", _TAHTON),
            "Every accent, and every maqaf with them — no difference anywhere the comparison"
            " reaches, though this Decalogue settles less"
            " than that suggests. In Exodus the two traditions accent the Shabbat commandment"
            " identically, so the only difference of accent it can adjudicate is the chanted"
            " verse boundary at עבדים. Koren takes the p-trad side of that, and of the"
            " traditions' one difference of vowel, the qamats/pataḥ of לא תרצח.",
        ),
        (
            "Deuteronomy main",
            "koren_dt_taxton",
            "280–281",
            ("p-trad ", _TAHTON),
            (
                "Every accent, every maqaf, and ",
                H.bold("this is the Decalogue that tests the claim"),
                f": in Deuteronomy the two {_TAHTON} strands part at ",
                H.bold(str(counts["total"])),
                " chanted words, and Koren takes the p-trad side of every one. ",
                H.bold(str(counts["total"] - counts["vocalization"])),
                " of them are differences of accent, which the transcription diffs; the last is"
                " the qamats/pataḥ of לא תרצח — a vowel, so outside what a transcription of"
                " accents records, and read off the page separately: Koren has the p-trad pataḥ. ",
                # The 7 Shabbat-commandment sites are the ones Exodus cannot reach: there the two
                # taxton strands are identical throughout that commandment (pdt's EX
                # decomposition, 4 boundary + 1 vocalization, leaves no remainder), which is what
                # the Exodus main row above means by settling less than it seems to.
                H.bold(str(counts["sabbath"])),
                " of them fall inside the Shabbat commandment, where Exodus reaches nothing at"
                " all; the ",
                link("companion page's appendix", _TAHTON_DETAILS_HREF),
                " catalogues them.",
            ),
        ),
        (
            "Exodus appendix",
            "koren_ex_elyon",
            "A38",
            ("p-trad ", _ELYON),
            (
                "Every chanted verse boundary, the whole disjunctive skeleton, and every chanted"
                " word marked as its Wikisource strand marks it but two. At יהיה and at ובנך that"
                " strand has a maqaf where Koren has a ",
                _ROM_MUNAX,
                " — one rung up the scale, so Koren separates into two chanted words what the"
                " Wikisource strand's maqaf makes one.",
            ),
        ),
        (
            "Deuteronomy appendix",
            "koren_dt_elyon",
            "A39",
            ("p-trad ", _ELYON),
            (
                "Every accent — and it joins both compounds its Exodus counterpart separates, so"
                " that separation is a fact about the one page rather than a habit of the"
                " edition. Its one difference is a maqaf, going the other way: Koren has"
                " לא־תעשה where its Wikisource strand has the two atoms apart, and keeps a ",
                _ROM_MUNAX,
                " on the joined לא even so. Both sides therefore have the same two accents, so"
                " this is a difference no accent can show: it was read off the page rather than"
                " found by the diff.",
            ),
        ),
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


# The boundary inside a chanted word, restored between the atoms after accents_and_letters
# reduces each atom to its letters and accents.
_MAQAF = "\N{HEBREW PUNCTUATION MAQAF}"


def _same_accent_on_two_atoms(shape: str) -> bool:
    """The survey shape of a compound with the same accent on two or more of its atoms.

    The strict half of ``maqaf_nonfinal_accents_page.pin_claims``' accented-alike criterion:
    that pin may drop the two-accent floor because MAM's prose verses have no one-accent
    compound either, but WLC's do (Joshua 20:4, whose compound's only accent sits on the
    non-final atom), and a floorless test here would sweep that in as a third "precedent".
    """
    accented = [a for a in shape.split("-") if a != "0"]
    return len(accented) >= 2 and len(set(accented)) == 1


def _wlc_munax_munax_compounds() -> tuple[str, str]:
    """The two WLC compounds with a munax on both atoms, lifted from the survey's tracked JSON.

    THE PRECEDENT SENTENCE IS DERIVED, NOT TYPED.  The conclusion says no maqaf compound of
    MAM's prose verses has the same accent on both atoms, and that WLC has that shape at
    exactly two places, a munax each time -- 1 Chronicles 27:14 and 2 Chronicles 1:11.  All
    of that is re-derived here from ``out/accgram/maqaf-nonfinal-accents.json``, the
    maqaf-nonfinal survey's own tracked record, raising on drift: a re-survey that moved
    either count fails the build rather than leave the sentence beside data that no longer
    says it.  The two displayed forms are the JSON's own words reduced to letters and accents
    with the maqaf restored -- 2 Chronicles 1:11's trailing paseq drops with the vowels, as
    in every accents_and_letters form.

    WHY THE PRECEDENT LIVES ON THIS PAGE.  The linked survey page once stated it, then was
    narrowed to MAM (4bc2d7f, f9d966d; Ben, 2026-07-26: "let's leave WLC (and indeed the LC)
    out of this"), leaving this page's "its precedent is a manuscript's" resting on nothing
    rendered and pinned by nothing (item 4 of ``doc/review-findings-2026-07-29.md``).  So the
    corpus split is drawn here: the survey page answers for MAM, and this derivation holds
    the WLC facts.
    """
    survey = json.loads(mpa.default_json_out_path().read_text(encoding="utf-8"))

    def occurrences(corpus: str) -> list[dict]:
        return survey["corpora"][corpus]["prose"]["occurrences"]

    mam_same = [
        o for o in occurrences("mam_simple") if _same_accent_on_two_atoms(o["shape"])
    ]
    assert not mam_same, mam_same
    hits = [o for o in occurrences("wlc422") if _same_accent_on_two_atoms(o["shape"])]
    assert [o["bcv"] for o in hits] == ["1c27:14", "2c1:11"], hits
    assert all(o["shape"] == "mun-mun" for o in hits), hits
    first, second = (
        _MAQAF.join(accents_and_letters(atom) for atom in o["word"].split(_MAQAF))
        for o in hits
    )
    return first, second


def _conclusion(
    verdicts: dict[str, tp.TranscriptionResult], counts: dict[str, int]
) -> tuple[object, ...]:
    chr1_form, chr2_form = _wlc_munax_munax_compounds()
    return (
        H.heading_level_2("Conclusion", {"id": "koren-conclusion"}),
        H.para(
            (
                "Koren follows the p-trad for the Decalogues, not the m-trad. The two traditions'"
                " most consequential divergence is over the opening span אנכי…מצותי — a"
                " divergence of chanted verse boundaries, which can be read off the accents on"
                " the span's two signal words, עבדים and על־פני. Koren lands on the p-trad side of"
                " that divergence on both strands: the p-trad ",
                _TAHTON,
                " in its Exodus",
                f" main Decalogue (pp. 113–114), and the p-trad {_ELYON} in its appendix"
                " Decalogue (p. A38).",
            )
        ),
        # The transcription verdicts (issue wlc-utils#69). The signal words place each Decalogue among the
        # four strands; only this says how far it then follows the Wikisource strand it was
        # placed in.
        H.para(
            (
                "How far each of the four Decalogues follows that strand is a separate question"
                " from which strand it is, and one the signal words cannot answer. The last"
                " column adds the question ",
                link("the companion page", _COMPANION_PAGE_HREF),
                " asks of the four idealized strands, asked here of what Koren actually has:"
                " run through the same prose grammar checker, does it parse?",
            )
        ),
        # Single-sourced in pds and stated verbatim on all three pages of the trio, here because
        # the table's middle column is written in its terms. Splice the constant; don't paraphrase.
        H.para((pds.MAQAF_IS_THE_LAST_RUNG,)),
        _verdict_table(verdicts, counts),
        # GUARDRAIL (2026-07-25 claim audit, findings 2 and 3). This paragraph made two claims that
        # the page's own evidence refuted.
        #
        # (1) "Three of the four follow their strand in every accent, and the fourth differs only
        # in how it divides two chanted words." The count is wrong: TWO of the four have a maqaf
        # difference -- besides the Exodus appendix's two splits, the Deuteronomy appendix one
        # joins לא־תעשה where its Wikisource strand leaves the atoms apart. The first fix went
        # further and declared a maqaf difference to be no accent difference at all, which
        # restored "all four follow their strand in every accent"; that convention is gone (see
        # the guardrail at pds.MAQAF_IS_THE_LAST_RUNG). Two of the four match mark for mark, two
        # differ at the maqaf, and neither claim may be dressed up as the other.
        #
        # (2) "no strand at all, in either tradition, separates יהיה from לך". Flatly false: all
        # four תחתון strands separate those two atoms, binding לא to יהיה (לא־יהיה, one chanted
        # word, merkha) and leaving לך alone with a tevir -- as the hub's own four-strands table
        # shows in its pT row, so the page a reader is sent to refuted the sentence. What is true,
        # and what the conclusion actually needs, is that no strand SPLITS THE COMPOUND יהיה־לך:
        # only the four עליון strands have that compound, and none of them divides it. Keep the
        # claim about the compound, and keep the תחתון strands' own division visible so the next
        # reader who checks the hub's table finds the two pages agreeing.
        H.para(
            (
                "Two of the four — the main Decalogues — match their Wikisource strand ",
                H.bold("mark for mark"),
                ". The other two part from theirs at the last rung only, each time at a maqaf:"
                " the Exodus appendix Decalogue separates both יהיה־לך and ובנך־ובתך, and the"
                " Deuteronomy appendix one joins לא־תעשה. Those are the mildest differences the"
                " scale has, and not one difference anywhere in the four takes the m-trad's side"
                " of anything. The separation of יהיה־לך in particular is Koren's own rather"
                " than a"
                f" tradition's: only the {_ELYON} strands have that compound at all — the ",
                _TAHTON,
                " strands instead bind לא to יהיה, leaving לך standing on its own with a ",
                _ROM_TEVIR,
                f" — and not one of the four {_ELYON} strands separates it. So that separation"
                " says nothing about which tradition Koren follows.",
            )
        ),
        # GUARDRAIL (item 4 of doc/review-findings-2026-07-29.md). This paragraph once promised
        # that the linked survey page "answers both" questions -- the rate AND the precedent,
        # a manuscript's included. The survey has since been narrowed to MAM's prose verses, so
        # its flat "no compound is accented alike twice" would sit beside a bare "not unheard
        # of" here as an apparent contradiction. The corpus split is therefore drawn in this
        # very paragraph -- MAM has no such compound, WLC has two -- and every quantifier in it
        # is re-derived from the survey's tracked JSON by _wlc_munax_munax_compounds, which
        # raises on drift.
        H.para(
            (
                "Joining לא־תעשה costs Koren nothing in accents because it keeps the ",
                _ROM_MUNAX,
                " on the לא it joins — and a joined atom that keeps its own accent is the rarer"
                " thing here, rarer than the maqaf difference itself. How rare it is in MAM's"
                " prose verses is counted on ",
                link("its own page", _MAQAF_NONFINAL_PAGE),
                ", and one shape the count comes back empty for is Koren's own: no maqaf"
                " compound of those verses has the same accent on both atoms. WLC — a corrected"
                " transcription of the Leningrad Codex — has that shape twice, with a ",
                _ROM_MUNAX,
                " on both atoms each time: at 1 Chronicles 27:14, ",
                hbo(chr1_form),
                ", and at 2 Chronicles 1:11, ",
                hbo(chr2_form),
                ". So Koren's compound is not unheard of — but its precedent is a manuscript's,"
                " and no printed edition is known to have one.",
            )
        ),
        # The grammaticality column (issue wlc-utils#52). All four agree with their Wikisource strand, so
        # what the column shows here is what following the p-trad elyon COSTS: the merged opening
        # verse the companion page's finding is about is on Koren's appendix pages, not only in an
        # idealized strand. The p. A38 note connection is deliberately stated as a coincidence of
        # subject rather than a grammatical motive -- the note argues from the count of
        # commandments.
        H.para(
            (
                "Under the checker, too, each of the four is exactly as grammatical as its"
                " Wikisource strand — and for the two appendix Decalogues that is worth spelling"
                " out, because that strand is ungrammatical. The p-trad ",
                _ELYON,
                " merges the first two commandments into one chanted verse, and that verse is the"
                " one the ",
                link("companion page's grammar check", _ELYON_FAILS_HREF),
                " rejects. Koren has it, in both books. So the companion page's finding is not"
                " a property of an idealized strand: it is on the page of a book in print. It is"
                " also, as it happens, the very reading the ",
                link("p. A38 note", f"#{_PA38_NOTE_ID}"),
                " above offers an alternative to — read the First Commandment in the ",
                _TAHTON,
                ", as its own chanted verse, and the merged verse never arises. The note argues"
                " from the count of ten commandments and says nothing about grammar, so this is a"
                " coincidence of subject rather than a grammatical motive; but the alternative it"
                " declines to print is the one the checker's objection points at.",
            )
        ),
        H.para(
            (
                "One scope note: the finding above rests on the אנכי…מצותי span — the most striking"
                " p-trad/m-trad divergence. Koren makes the same p-trad choice at that span in both"
                " of its Decalogues: the Exodus one and the",
                f" Deuteronomy (Vaetḥanan) one, whose {_TAHTON} main Decalogue starts on p. 280"
                " and runs onto"
                " p. 281. There too אנכי…עבדים is its own chanted verse, closing on עבדים with a",
                *[" ", _ROM_SILLUQ_SOF_PASUQ, "."],
            )
        ),
        H.para(
            (
                "Koren's Deuteronomy also reaches a divergence its Exodus Decalogue cannot: the"
                " Shabbat commandment, where the p-trad and m-trad part again. There too Koren"
                " has the p-trad — so its p-trad allegiance is unqualified, where the ",
                link("Simanim page", _SIMANIM_PAGE),
                " finds Simanim's Tiqqun following the m-trad accents at that very commandment"
                " (an accents-only departure — Simanim's Tiqqun still follows the p-trad's"
                " chanted verse boundaries). So Koren happens to be pure p-trad at both"
                " divergence points, where Simanim's Tiqqun is not — and it is exactly that"
                " kind of impurity the Shabbat commandment's own signal words exist to catch,"
                " since an accents-only departure moves no chanted verse boundary and so leaves"
                " עבדים and על־פני reading p-trad throughout. The scan"
                " below is that commandment, with "
                # Single-sourced in pds and shared with the Simanim page's matching scope note;
                # the complementary-jobs doctrine is spelled out at that constant.
                + pds.SHABBAT_SIGNAL_SHORTHAND
                + ". In Koren's p-trad they have, respectively, a ",
                _ROM_GERESH,
                ", a ",
                _ROM_REVIA,
                ", and a ",
                _ROM_ZAQEF_QATAN,
                "; the ",
                link("companion page's appendix", _TAHTON_DETAILS_HREF),
                " has the full details. The Deuteronomy half of the claim no longer rests on the ",
                _TAHTON,
                " alone: Koren's Deuteronomy ",
                _ELYON,
                ", in its appendix (p. A39), has since been transcribed too, and follows the"
                " p-trad in every accent.",
            )
        ),
        mhi.scan_figure(
            _P281_DT_BODY_IMG,
            "Koren p. 281: the Shabbat commandment of the Deuteronomy Decalogue, in the p-trad"
            " taḥton",
            (
                "The Shabbat commandment of Koren's Deuteronomy (Vaetḥanan) main Decalogue"
                f" (p. 281), in the p-trad {_TAHTON}. The three signal words are highlighted.",
            ),
            img_class="ink-on-white",
            width=None,
            boxes=_P281_BOXES,
            viewbox=(913, 186),
        ),
    )


def render_body_contents(
    source: dict,
    results: list[pd.VersionResult],
    verdicts: dict[str, tp.TranscriptionResult],
) -> tuple[object, ...]:
    # ``results`` is here only for this call, and it is the reason the verdict table can state how
    # many ways the two Deuteronomy תחתון strands part: the count is re-derived from the vendored
    # words on every generation and raises unless the divergence set is still the pinned one. It
    # was a typed "five" until the 2026-07-25 claim audit found no two pages of the trio agreeing
    # on it -- see printed_decalogue_taxton_diff.
    counts = pdt.dt_taxton_diff_counts(results)
    return (
        *_intro(source),
        *_pa38_note_section(),
        *_conclusion(verdicts, counts),
    )


def default_html_out_path(repo_root: Path) -> Path:
    return paths.wlc_pages_dir() / "accgram" / "printed-decalogue-koren.html"


def add_args(parser: argparse.ArgumentParser, repo_root: Path) -> None:
    parser.add_argument("--source", type=Path, default=pd.default_source_path())
    parser.add_argument(
        "--html-out", type=Path, default=default_html_out_path(repo_root)
    )


def run(args: argparse.Namespace) -> None:
    # The four-strands table lives on the companion page, so this page tabulates none of the
    # strands' own verdicts -- but it does need them, since the verdict table's last column states
    # each transcription's verdict AGAINST its Wikisource strand's (issue wlc-utils#52). Both checks
    # together are a fraction of a second, so nothing here is worth skipping for regeneration
    # speed.
    source = pd.load_source(args.source)
    results = pd.check_all(source)
    verdicts = tvc.by_stem(tp.check_all(results))

    html_out: Path = args.html_out
    html_out.parent.mkdir(parents=True, exist_ok=True)
    H.write_html_to_file(
        body_contents=render_body_contents(source, results, verdicts),
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
