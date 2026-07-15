"""Render the generated versification-and-cantillation HTML document.

Prose is authored here; the Hebrew example words are pulled byte-faithfully from
the upstream MAM-parsed-plus data via `strands.gather_examples` so the generated
output stays in lockstep with the source text.

The document is a standalone HTML page (it is served via GitHub Pages at
https://bdenckla.github.io/MAM-simple/versification-and-cantillation.html),
so it carries its own <head> and links its own stylesheet
(versification-and-cantillation.css, deployed alongside it by generate_doc.py)
rather than relying on GitHub's Markdown viewer.

On rolling our own HTML (a deliberate choice, not ignorance of `mb_misc.mb_html`):
this page is authored *prose with holes* — multi-paragraph English/Hebrew text with
dense inline markup (<em>/<strong>/<code>/<blockquote>) and only a handful of
`{placeholder}` slots filled from data. That is a template-fill problem, for which a
`str.format` template is idiomatic. `mb_html` is the wrong tool here: it is a
tree-builder for *data-driven* HTML (build structure from records via htel_mk /
table_row_of_data), so expressing authored prose through it would bury the prose in
nested calls; worse, its whitespace assertions (no double spaces, no leading/trailing
space in text nodes) are sane for tokenized Hebrew data but hostile to free prose.
This file also began life as a Markdown generator (render_full_markdown) and was
ported to HTML only when it needed a Pages-served <head>/CSS, which is why the body
reads as authored markup rather than assembled elements. (The mpplus_*.py diff-report
generators likewise bypass `mb_html`, for their own — different — reasons.)

Editing note: the rendered output is a *snapshot* — tests/test_versification_and_cantillation_doc.py
asserts it byte-for-byte against the deployed MAM-simple/gh-pages/ copy. So any edit here,
in strands.py, or in the .css (whose source of truth is the copy beside this file, NOT the
gh-pages copy — that one is overwritten on regen) is a no-op (and turns that test red)
until you regenerate the deployed files. Regenerate via the CLI subcommand, from the repo
root: `.venv/Scripts/python.exe py/main_mam_simple.py doc-only` (alias `doc`). That drives
generate_doc.write_output_if_changed() for this doc and the sibling versification-
differences doc together; don't hand-roll a one-off regen script. Then run the suite from
the repo root via `py/main_test.py` (a bare `pytest` has no mb_cmn on sys.path). The Hebrew
example words are not authored here — they come from strands.gather_examples; see that module.
"""

from pathlib import Path

from mb_cmn import provenance
from versification_and_cantillation import strands

_GENERATOR_FILE = Path(__file__).with_name("generate_doc.py")

# The sibling versification-differences doc stays Markdown, rendered on github.com;
# from this Pages-served HTML page we therefore link to its rendered blob view.
_VDIFF_URL = (
    "https://github.com/bdenckla/MAM-simple/blob/main/doc/versification-differences.md"
)

# The MAM-with-doc FOI page listing verses with a פסקא באמצע פסוק (mid-verse
# samekh/pe divider); linked from the body as the catalogue of such verses.
_PBP_FOI_URL = (
    "https://bdenckla.github.io/MAM-with-doc/foi/foi-rare-tmpls.html#intro-col-e-sampe"
)

# The MAM-with-doc rendering of 1 Samuel 16:12, the {petuxah}-form פסקא באמצע פסוק
# cited in the body as a plainer counterpart to the Numbers case. Per-verse anchors
# on those book pages are "c{chapter}v{verse}".
_1SAM_16_12_URL = "https://bdenckla.github.io/MAM-with-doc/BA-1Samuel.html#c16v12"

# The sibling wlc-utils gh-pages report on whether the printed tradition's Decalogue
# cantillation is grammatical. Cross-repo, so an absolute Pages URL (the gh-pages/
# segment is dropped in the served URL). Linked from the Decalogue-background aside.
_PRINTED_DECALOGUE_URL = (
    "https://bdenckla.github.io/wlc-utils/accgram/printed-decalogue.html"
)

# Romanized (transliterated) Hebrew terms named throughout the body and tables. Each is
# styled the same way at every mention, so — like the two cantillation strands, which are
# just two more such terms — the markup lives here in one place, abstracted behind {curly}
# placeholders filled from _ROMANIZED, rather than being hand-written at each mention. This
# mirrors mb_author/author.py's $-substituted _ROMANIZED dict (a different substitution
# syntax, same idea); here we stay with str.format's {curly} placeholders, the scheme the
# rest of this template already uses.
#
# Centralizing the wrapper keeps the markup *choice* in one place. It emits a
# <span class="romanized"> — styled italic via span.romanized in the CSS (see
# versification-and-cantillation.css) — matching how the repo's other generated docs mark
# romanized Hebrew (mb_author/author.py, mb_misc/styles_authored.css, and the sibling
# gh-pages stylesheets). An <em> gloss was the earlier form here, but it was never semantic:
# we are not emphasizing these words, only marking them as transliterated. (Genuine emphasis
# in the prose still uses <em> directly.)
#
# ASCII keys spell the letter xet (ח) as x (repo convention, cf. author.py's $tarxa / $patax);
# the displayed value spells it as precomposed h-with-dot-below = U+1E25 (NFC, issue #187).
# The keys are exactly the {placeholder} names used in _BODY_TEMPLATE and the table templates.
def _romanized(term):
    return f'<span class="romanized">{term}</span>'


_ROMANIZED = {
    key: _romanized(term)
    for key, term in {
        "taxton": "taḥton",
        "elyon": "elyon",
        "etnaxta": "etnaḥta",
        "sof_pasuq": "sof pasuq",
        "petuxah": "petuḥah",
        "setumah": "setumah",
    }.items()
}

# The external stylesheet, linked from the <head> and deployed next to the HTML
# (same basename, sibling file in gh-pages/) by generate_doc.py. The CSS lives in
# its own .css file — not a string here — because it is static (no interpolation,
# unlike _BODY_TEMPLATE below), so it is better edited/linted as real CSS.
CSS_FILENAME = "versification-and-cantillation.css"

# str.format template for the <body> contents. The only braces are the
# {placeholders} below; all Hebrew example words are substituted from data. Latin
# transliteration uses precomposed "h with dot below" (U+1E25 = NFC), per issue #187.
#
# Terminology convention (keep consistent): the scheme-noun is "versification", never
# "numbering" (the latter word is deliberately absent). Kept and distinct: "numbered
# verse" (a defined term) and the act-verbs "numbers at" / "places a number at".
_BODY_TEMPLATE = """\
<h1>Versification and Cantillation</h1>

<p>This document is a companion to <a href="{vdiff_url}">versification-differences.md</a>.
That document deliberately ignores cantillation,
defining a verse as simply a span of text between two cv-labels.
That definition of a verse is what we will call
a <strong>numbered verse</strong> in this document.
In this document, we will not ignore cantillation,
and it will be important to make a distinction
between a numbered verse and a <strong>chanted verse</strong>.
We define a chanted verse as a span of text between two {sof_pasuq} marks,
whose accents are intended to obey the rules of cantillation.
(By this definition,
a dually-cantillated span between two {sof_pasuq} marks is not a chanted verse,
although at least one of its strands is,
if both {sof_pasuq} marks belong to that strand.)</p>

<p>In cases that are rare, but central to this document,
a numbered verse is not a chanted verse.
This happens mostly (and unavoidably) in the Decalogues,
where, no matter what versification is used,
some numbered verses are not chanted verses
in at least one of the two strands of cantillation.
Different trade-offs in the face of this "impossible" situation
give rise to different versifications of the Decalogues.</p>

<p>Aside: like many numbered verses of the Decalogues,
Gen. 35:22 has two strands of cantillation
and is only a chanted verse in one of those two strands.
(In the other strand, it contains two chanted verses in their entirety.)
Unlike in the Decalogues, at Gen. 35:22
all versifications discussed here (MAM, BHS, and Sefaria)
make the same trade-off in the face of this "impossible" situation:
they all agree to label Gen. 35:22 as a single numbered verse.</p>

<p>Other than the cases in the Decalogues,
the one other case in our versifications
where a numbered verse is not a chanted verse
is the Num. 25/26 break in BHS versification.
Beyond that shared trait, this case has little in common with the Decalogue cases:
here there is only one strand of cantillation,
and, as we will see, no versification is forced to let a numbered verse
fail to be a chanted verse — BHS simply does.
BHS splits the chanted verse that MAM calls Num. 26:1 into
a 25:19 span (a cv-label that does not exist in MAM)
and a 26:1 span.
BHS 26:1 starts right after an {etnaxta}.</p>

<h2>The Decalogues: background</h2>

<p>Each of the Decalogues has two parallel strands of cantillation.
The <strong>{taxton}</strong> (תחתון) strand
divides the passage into twelve chanted verses.
The <strong>{elyon}</strong> (עליון) strand
divides the passage into ten chanted verses: the Ten Commandments.
Relative to the {taxton}, the lengths of the {elyon} verses are uneven.
There are two {elyon} verses that are quite long, containing, respectively "three and a half" and four {taxton} verses.
(That "half" will be explained below.)
In contrast, there are four consecutive {elyon} verses that are very short:
all four are contained within a single {taxton} verse.</p>

<p>Aside: this document is only concerned with the cantillation of the Decalogues
in the manuscript tradition;
whether the cantillation of the Decalogues in the <em>printed</em> tradition is even
grammatical is examined in a separate report,
<a href="{printed_decalogue_url}">In the printed tradition, are the accents of the
Decalogue grammatical?</a></p>

<h2>The Decalogues: two versification policies</h2>

<p>In the Decalogues, our versifications differ only in which chanted verses start with a cv-label:</p>

<ul>
  <li><strong>MAM</strong> places a cv-label at the start of every {taxton} verse.</li>
  <li><strong>BHS</strong> places a cv-label at the start of every {taxton} <strong>or</strong> {elyon} verse —
  the union of the two cantillations' verse boundaries.</li>
  <li><strong>Sefaria</strong> is a mix of MAM and BHS:
  it places a cv-label at the start of every {taxton} verse,
  and at the start of some but not all {elyon} verses.</li>
</ul>

<p>From here on we discuss only MAM and BHS: describing Sefaria in detail adds
nothing of interest, since it is merely a mix of the two. The Sefaria details
can be found in the <a href="{vdiff_url}">companion document</a>.</p>

<h3>The early drift</h3>

<p>When an {elyon} verse contains only part of a {taxton} verse,
the BHS numbering drifts forward relative to MAM.
The table below shows the first of two such drifts in the Decalogues.
A span of two {elyon} verses contains four {taxton} verses in their entirety,
but they are not contained "nicely", for the reasons listed below.
</p>
<ul>
  <li>
    The {elyon} verse {early_elyon_short_verse} contains only the first "half" of the {taxton} verse {early_taxton_split_verse}.
  </li>
  <li>The {elyon} verse {early_elyon_long_verse} contains "three and a half" {taxton} verses. The {elyon} contains:
    <ul>
      <li>The second "half" of the {taxton} verse {early_taxton_split_verse}.</li>
      <li>Three whole {taxton} verses.</li>
    </ul>
  </li>
</ul>

{early_strand_table}

<p>In the table above, each chanted verse's first and last word
is shown in green and red respectively.
Also, a schematic version of each chanted verse is shown at the bottom of the table,
as a green-to-red color gradient.
All examples in the body of this document are from the <strong>Exodus</strong> Decalogue;
the <a href="#appendix-deuteronomy">appendix</a> revisits these points in the Deuteronomy Decalogue,
whose chanted verse structure is the same,
with the numbered verse boundaries falling at the same places in it,
despite some differences in the details of its text that are unimportant to our basic points here.</p>

<h3>The middle no-drift case</h3>

<p>When an {elyon} verse contains multiple {taxton} verses in their entirety,
there is no numbering drift between MAM and BHS.
This is the case with the four consecutive {taxton} verses in the table below,
although unfortunately the point is somewhat muddied
by a drift that has already happened, which we described above.</p>

{sab_table}

<h3>The late drift</h3>

<p>When an {elyon} verse contains only part of a {taxton} verse,
the BHS numbering drifts forward relative to MAM.
The table below shows a drift due to
four {elyon} verses each containing only a "quarter" of a {taxton} verse.
</p>

{late_table}

<h2>Num. 25/26: a break at an {etnaxta}, not a {sof_pasuq}</h2>

<p>Here there is only one cantillation,
and BHS starts a numbered verse in the middle of a chanted verse,
right after an {etnaxta}.</p>

<p>MAM keeps Num. 26:1 as a single chanted verse with a
mid-verse paragraph break inside it
— a פסקא באמצע פסוק (in its {petuxah} form).
The break is shown below as a line break,
which is what a {petuxah} ("open" section) in fact is
(with some qualifications we won't get into).
Both lines are part of a single chanted verse.</p>

<blockquote class="verse">
{num_seg0}<br>
{num_seg1_first} … {num_seg1_last}
</blockquote>

<p>The chanted verse ends, as always, at {sof_pasuq} ({num_seg1_last}).
The word before the break, {num_seg0_last}, has only {etnaxta} —
the strongest mid-verse disjunctive, but not a verse-ending accent.
BHS further emphasizes that break by
making its 25:19 end at {num_seg0_last} —
on an {etnaxta}, <strong>not</strong> a {sof_pasuq}.
So BHS's 25:19 is not a chanted verse.</p>

<p>Why did BHS choose to start a numbered verse (and a chapter!) here?
The {etnaxta} and its accompanying פסקא באמצע פסוק already signal a strong break here;
perhaps someone nonetheless felt that a chapter break was needed
to emphasize the break at this point.
Or perhaps this chapter break has its origin in a non-cantillated
(perhaps even non-Hebrew) version of the text,
where the cantillation-location of a chapter break is irrelevant
(or at least invisible).</p>

<p>Note that the פסקא באמצע פסוק does not explain the chapter break.
Even in the {petuxah} form it takes here,
this Numbers case is the only place in which פסקא באמצע פסוק causes a numbered verse break,
much less a chapter break,
in any of our versifications.
(The פסקא באמצע פסוק phenomenon also has a {setumah} form,
which is considered a weaker break than the {petuxah} form.)
See, for example, <a href="{sam_16_12_url}">1 Samuel 16:12</a> — one of <a href="{pbp_foi_url}">many such verses</a>.
(This is just one of nine cases of {petuxah}-form פסקא באמצע פסוק in the book of Samuel,
out of twenty-four such cases in all of Tanakh.
For some reason, this rare type of break is overrepresented in the book of Samuel.)</p>

<p>Why, then, does MAM not follow BHS here?
Unlike the question of BHS's motive, this one cantillation can answer.
BHS's break creates a numbered verse that is not a chanted verse:
its 25:19, which ends at {etnaxta}.
In the Decalogues no versification can avoid such a verse
— that is the "impossible" situation described above —
but here avoiding it is entirely possible, and MAM avoids it.
So, although <em>ignoring</em> cantillation may be what allowed BHS's break,
a refusal to ignore cantillation
— in particular, a refusal to have a numbered verse that is not also a chanted verse —
is what may have made a versification like MAM's resist that break.</p>

<h2 id="appendix-deuteronomy">Appendix: the same points in Deuteronomy</h2>

<p>Every example above is drawn from the <strong>Exodus</strong> Decalogue. The
Deuteronomy Decalogue (MAM 5:6–5:17) has the same two strands of cantillation
with the same chanted verse structure, so the same points hold there.
What differs are aspects of the wording
(substituted words, added phrases)
that leave those cantillation and versification points intact.
The numbered verse boundaries still fall at the same places in the chanted verse structure.
This appendix shows the two places where that wording difference is visible.
In the tables below a word is
<span class="vc-mid vc-agree">washed out</span>
when it is identical to its Exodus counterpart and shown at
<span class="vc-mid">full strength</span>
when it differs, so the eye lands on the differences;
first/last words keep their green/red hue,
paled when they match Exodus.</p>

<p>The <strong>early split</strong> is not shown again here: through MAM's Deut. 5:9 the
first and last words of the chanted verses are the same as those in Exodus,
so its table would be uniformly washed out.
(Words other than those first and last ones do differ — a dropped and an added
connective vav, one plene spelling — but those words never reach this
boundary-only table.)
The differences live almost entirely in the <em>Sabbath</em> commandment,
with only a connective vav and one substituted word in the <em>late split</em>.</p>

<h3>The Sabbath — a different, longer text</h3>

<p>Deuteronomy's Sabbath commandment opens with שמור (not Exodus's זכור) and is
considerably longer, so although the {taxton}/{elyon} chanted verse structure is unchanged — one
{elyon} verse spanning four {taxton} verses, exactly as in Exodus — most of the boundary
words differ:</p>

{deut_sab_table}

<p>Only the second {taxton} verse (MAM 5:12) matches Exodus at both ends. The first (5:11) and
fourth (5:14) differ at both ends; the third (5:13) shares its first word (ויום) but not its
last word — Deuteronomy runs on past Exodus's בשעריך to כמוך.</p>

<h3>The late split — nearly identical</h3>

<p>Here the two Decalogues read very nearly alike. Deuteronomy joins the commandments with
a connective vav (וְלֹא, "and you shall not") where Exodus sets them without it, and its
ninth commandment ends עֵד שָׁוְא where Exodus has עֵד שָׁקֶר. Those wording differences
aside, the {taxton}/{elyon} chanted verse structure — four {elyon} verses nested in one {taxton} verse,
all ending together — is unchanged, so only וְלֹא and שָׁוְא stand at full strength while
everything matching Exodus washes out:</p>

{deut_late_table}
"""

# The document's tables live here as their own str.format templates rather than inline in
# _BODY_TEMPLATE above, so the authored prose reads top-to-bottom without the
# placeholder-dense table markup breaking the flow (the tables can't be read in source
# anyway — nearly every cell is a {placeholder} filled from data). render_full_html fills
# each table over the same `fields` dict, then splices the rendered HTML into
# _BODY_TEMPLATE via matching {..._table} placeholders (a second format pass — safe
# because the rendered tables contain no braces of their own).

# MAM 20:7-20:10 (the Sabbath commandment): the {taxton} reads four verses, the {elyon}
# one verse spanning all four (green start on 20:7, red stop on 20:10, interior plain).
_SAB_TABLE = """\
<table dir="rtl">
  <tr>
    <th><abbr title="elyon cantillation strand">E</abbr></th>
    <td>{sab_elyrow_7}</td>
    <td>{sab_elyrow_8}</td>
    <td>{sab_elyrow_9}</td>
    <td>{sab_elyrow_10}</td>
  </tr>
  <tr>
    <th><abbr title="taḥton cantillation strand">T</abbr></th>
    <td>{sab_taxrow_7}</td>
    <td>{sab_taxrow_8}</td>
    <td>{sab_taxrow_9}</td>
    <td>{sab_taxrow_10}</td>
  </tr>
  <tr class="cv">
    <th><abbr title="MAM verse number">M</abbr></th>
    <td>20:7</td>
    <td>20:8</td>
    <td>20:9</td>
    <td>20:10</td>
  </tr>
  <tr class="cv">
    <th><abbr title="BHS verse number">B</abbr></th>
    <td>20:8</td>
    <td>20:9</td>
    <td>20:10</td>
    <td>20:11</td>
  </tr>
  <tr>
    <th><abbr title="schematic color gradient for the elyon verse">e</abbr></th>
    <td class="vc-grad" colspan="4"></td>
  </tr>
  <tr>
    <th><abbr title="schematic color gradient for the taḥton verse(s)">t</abbr></th>
    <td class="vc-grad"></td>
    <td class="vc-grad"></td>
    <td class="vc-grad"></td>
    <td class="vc-grad"></td>
  </tr>
</table>"""

# The early split as a single transposed table (Sabbath-table style): the taxton and elyon
# strands across the top, MAM and BHS verse numbers below, over the four consecutive taxton
# verses 20:2-20:5. The lone elyon boundary inside MAM 20:2 splits it into 20:2a/20:2b —
# where BHS gains a verse and the numbering drifts +1 (MAM's one 20:2 spans both columns,
# shown by the colspan; by 20:5 BHS has already advanced to 20:6).
_EARLY_STRAND_TABLE = """\
<table dir="rtl">
  <tr>
    <th><abbr title="elyon cantillation strand">E</abbr></th>
    <td>{early_elyrow_202a}</td>
    <td>{early_elyrow_202b}</td>
    <td>{early_elyrow_203}</td>
    <td>{early_elyrow_204}</td>
    <td>{early_elyrow_205}</td>
  </tr>
  <tr>
    <th><abbr title="taḥton cantillation strand">T</abbr></th>
    <td>{early_taxrow_202a}</td>
    <td>{early_taxrow_202b}</td>
    <td>{early_taxrow_203}</td>
    <td>{early_taxrow_204}</td>
    <td>{early_taxrow_205}</td>
  </tr>
  <tr class="cv">
    <th><abbr title="MAM verse number">M</abbr></th>
    <td colspan="2">20:2</td>
    <td>20:3</td>
    <td>20:4</td>
    <td>20:5</td>
  </tr>
  <tr class="cv">
    <th><abbr title="BHS verse number">B</abbr></th>
    <td>20:2</td>
    <td>20:3</td>
    <td>20:4</td>
    <td>20:5</td>
    <td>20:6</td>
  </tr>
  <tr>
    <th><abbr title="schematic color gradient for the elyon verse">e</abbr></th>
    <td class="vc-grad"></td>
    <td class="vc-grad" colspan="4"></td>
  </tr>
  <tr>
    <th><abbr title="schematic color gradient for the taḥton verse(s)">t</abbr></th>
    <td class="vc-grad" colspan="2"></td>
    <td class="vc-grad"></td>
    <td class="vc-grad"></td>
    <td class="vc-grad"></td>
  </tr>
</table>"""

# The late split (Exod 20:12), transposed like _SAB_TABLE but mirrored: the taxton is the
# single verse spanning all four columns (green start on 20:12's first word, red stop on
# שקר, interior plain), while each of the four short commandments is its own elyon verse.
# The columns are those commandments in scripture order. MAM keeps one number (colspan),
# BHS numbers each elyon start (four verses).
_LATE_TABLE = """\
<table dir="rtl">
  <tr>
    <th><abbr title="elyon cantillation strand">E</abbr></th>
    <td>{late_elyrow_0}</td>
    <td>{late_elyrow_1}</td>
    <td>{late_elyrow_2}</td>
    <td>{late_elyrow_3}</td>
  </tr>
  <tr>
    <th><abbr title="taḥton cantillation strand">T</abbr></th>
    <td>{late_taxrow_0}</td>
    <td>{late_taxrow_1}</td>
    <td>{late_taxrow_2}</td>
    <td>{late_taxrow_3}</td>
  </tr>
  <tr class="cv">
    <th><abbr title="MAM verse number">M</abbr></th>
    <td colspan="4">20:12</td>
  </tr>
  <tr class="cv">
    <th><abbr title="BHS verse number">B</abbr></th>
    <td>20:13</td>
    <td>20:14</td>
    <td>20:15</td>
    <td>20:16</td>
  </tr>
  <tr>
    <th><abbr title="schematic color gradient for the elyon verse">e</abbr></th>
    <td class="vc-grad"></td>
    <td class="vc-grad"></td>
    <td class="vc-grad"></td>
    <td class="vc-grad"></td>
  </tr>
  <tr>
    <th><abbr title="schematic color gradient for the taḥton verse(s)">t</abbr></th>
    <td class="vc-grad" colspan="4"></td>
  </tr>
</table>"""

# Appendix — the Deuteronomy Sabbath (MAM 5:11–5:14), same shape as _SAB_TABLE but with
# Deut's own words (shaded agree/differ vs Exodus) and Deut verse numbers.
_DEUT_SAB_TABLE = """\
<table dir="rtl">
  <tr>
    <th><abbr title="elyon cantillation strand">E</abbr></th>
    <td>{deut_sab_elyrow_11}</td>
    <td>{deut_sab_elyrow_12}</td>
    <td>{deut_sab_elyrow_13}</td>
    <td>{deut_sab_elyrow_14}</td>
  </tr>
  <tr>
    <th><abbr title="taḥton cantillation strand">T</abbr></th>
    <td>{deut_sab_taxrow_11}</td>
    <td>{deut_sab_taxrow_12}</td>
    <td>{deut_sab_taxrow_13}</td>
    <td>{deut_sab_taxrow_14}</td>
  </tr>
  <tr class="cv">
    <th><abbr title="MAM verse number">M</abbr></th>
    <td>5:11</td>
    <td>5:12</td>
    <td>5:13</td>
    <td>5:14</td>
  </tr>
  <tr class="cv">
    <th><abbr title="BHS verse number">B</abbr></th>
    <td>5:12</td>
    <td>5:13</td>
    <td>5:14</td>
    <td>5:15</td>
  </tr>
  <tr>
    <th><abbr title="schematic color gradient for the elyon verse">e</abbr></th>
    <td class="vc-grad" colspan="4"></td>
  </tr>
  <tr>
    <th><abbr title="schematic color gradient for the taḥton verse(s)">t</abbr></th>
    <td class="vc-grad"></td>
    <td class="vc-grad"></td>
    <td class="vc-grad"></td>
    <td class="vc-grad"></td>
  </tr>
</table>"""

# Appendix — the Deuteronomy late split (5:16), same shape as _LATE_TABLE, its words shaded
# against their Exodus twins (agree = washed out). Deut differs at the connective וְ on the
# 2nd–4th commandments (וְלֹא vs Exodus's לֹא) and the ninth's end-word (שָׁוְא vs שָׁקֶר),
# so only those forms stay full-strength; everything else washes out.
_DEUT_LATE_TABLE = """\
<table dir="rtl">
  <tr>
    <th><abbr title="elyon cantillation strand">E</abbr></th>
    <td>{deut_late_elyrow_0}</td>
    <td>{deut_late_elyrow_1}</td>
    <td>{deut_late_elyrow_2}</td>
    <td>{deut_late_elyrow_3}</td>
  </tr>
  <tr>
    <th><abbr title="taḥton cantillation strand">T</abbr></th>
    <td>{deut_late_taxrow_0}</td>
    <td>{deut_late_taxrow_1}</td>
    <td>{deut_late_taxrow_2}</td>
    <td>{deut_late_taxrow_3}</td>
  </tr>
  <tr class="cv">
    <th><abbr title="MAM verse number">M</abbr></th>
    <td colspan="4">5:16</td>
  </tr>
  <tr class="cv">
    <th><abbr title="BHS verse number">B</abbr></th>
    <td>5:17</td>
    <td>5:18</td>
    <td>5:19</td>
    <td>5:20</td>
  </tr>
  <tr>
    <th><abbr title="schematic color gradient for the elyon verse">e</abbr></th>
    <td class="vc-grad"></td>
    <td class="vc-grad"></td>
    <td class="vc-grad"></td>
    <td class="vc-grad"></td>
  </tr>
  <tr>
    <th><abbr title="schematic color gradient for the taḥton verse(s)">t</abbr></th>
    <td class="vc-grad" colspan="4"></td>
  </tr>
</table>"""

# Filled over the same `fields` dict, then spliced into _BODY_TEMPLATE by these keys.
_TABLE_TEMPLATES = {
    "sab_table": _SAB_TABLE,
    "early_strand_table": _EARLY_STRAND_TABLE,
    "late_table": _LATE_TABLE,
    "deut_sab_table": _DEUT_SAB_TABLE,
    "deut_late_table": _DEUT_LATE_TABLE,
}


def render_full_html(books_mpu):
    examples = strands.gather_examples(books_mpu)
    fields = {
        "vdiff_url": _VDIFF_URL,
        "pbp_foi_url": _PBP_FOI_URL,
        "sam_16_12_url": _1SAM_16_12_URL,
        "printed_decalogue_url": _PRINTED_DECALOGUE_URL,
        **_ROMANIZED,
        **examples,
    }
    comment = provenance.generated_html_comment(_GENERATOR_FILE)
    tables = {name: tmpl.format(**fields) for name, tmpl in _TABLE_TEMPLATES.items()}
    body = _BODY_TEMPLATE.format(**fields, **tables)
    return (
        "<!doctype html>\n"
        f"<!-- {comment} -->\n"
        '<html lang="en">\n'
        "<head>\n"
        '<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        "<title>Versification and Cantillation</title>\n"
        f'<link rel="stylesheet" href="{CSS_FILENAME}">\n'
        "</head>\n"
        "<body>\n"
        f"{body}"
        "</body>\n"
        "</html>\n"
    )
