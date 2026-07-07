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

# The two Decalogue cantillation strands, named inline throughout the body. Each
# is styled the same way at every mention (an <em> gloss of the Hebrew term), so
# the styling lives here in one place rather than being repeated at each mention.
_TAXTON = "<em>taḥton</em>"
_ELYON = "<em>elyon</em>"

# The external stylesheet, linked from the <head> and deployed next to the HTML
# (same basename, sibling file in gh-pages/) by generate_doc.py. The CSS lives in
# its own .css file — not a string here — because it is static (no interpolation,
# unlike _BODY_TEMPLATE below), so it is better edited/linted as real CSS.
CSS_FILENAME = "versification-and-cantillation.css"

# str.format template for the <body> contents. The only braces are the
# {placeholders} below; all Hebrew example words are substituted from data. Latin
# transliteration uses precomposed "h with dot below" (U+1E25 = NFC), per issue #187.
_BODY_TEMPLATE = """\
<h1>Versification and Cantillation</h1>

<p>This document is a companion to <a href="{vdiff_url}">versification-differences.md</a>.
That document deliberately ignores cantillation,
treating a "verse" as nothing more than a span of text between two cv-labels.
That definition of a verse is what we will call a "numbered verse" in this document.
In this document we will not ignore cantillation,
and it will be important to make a distinction between a numbered verse and a chanted verse.
We define a chanted verse as a span of text between two sof pasuq marks,
where that span's accents obey the rules of cantillation.</p>

<p>In cases that are rare, but central to this document,
a numbered verse is not a chanted verse.
This happens mostly (and unavoidably) in the Decalogues,
where, no matter what versification is used,
some numbered verses are not chanted verses
in at least one of the two strands of cantillation.
Different trade-offs in the face of this "impossible" situation
give rise to different versifications of the Decalogues.</p>

<p>(Aside: like many numbered verses of the Decalogues,
Genesis 35:22 has two strands of cantillation
and is only a chanted verse in one of those two strands.
(In the other strand, it contains two chanted verses in their entirety.)
Unlike in the Decalogues, at Genesis 35:22
all versifications discussed here (MAM, BHS, and Sefaria)
make the same trade-off in the face of this "impossible" situation:
they all agree to label Genesis 35:22 as a single numbered verse.)</p>

<p>Other than the cases in the Decalogues,
the one other case in our versifications (MAM, BHS, and Sefaria)
where a numbered verse is not a chanted verse
is the Numbers 25/26 boundary in BHS versification.
This case has little in common with the cases in the Decalogues.
BHS splits the chanted verse that MAM calls Numbers 26:1 into
a 25:19 span (a cv-label that does not exist in MAM)
and a 26:1 span.
BHS 26:1 starts right after an <em>etnaḥta</em>.</p>

<h2>The Decalogues: background</h2>

<p>Each of the Decalogues carries <strong>two</strong> parallel strands of cantillation.
The <strong>lower</strong> ({taxton}, תחתון) strand
divides the passage into twelve ordinary-length chanted verses.
The <strong>upper</strong> ({elyon}, עליון) strand
has a different division of the text.
The {elyon} divides the passage into <strong>ten</strong> chanted verses,
each traditionally construed as one of the Ten Commandments.
To land on ten, it does two complementary things.
Toward the end it makes four very short (two-word) verses, giving
"You shall not murder / commit adultery / steal / bear false witness" a verse each.
Toward the beginning it does the opposite, merging what the {taxton} reads as
several verses into one very long verse —
and it does this a second time, later, for the Sabbath commandment.
The long verses pay for the short ones:
without the merges, the four extra short verses would push the count past ten.
The {taxton}, by contrast, ignores the ten-commandment grouping
and divides the same text into <strong>twelve</strong> ordinary-length verses.</p>

<p>MAM versifies the Decalogues
according to the chanted verses of the <strong>lower</strong> cantillation.
In the MAM-simple data these strands are the
<code>cant-alef</code> (lower / {taxton})
and
<code>cant-bet</code> (upper / {elyon}) elements.
(The <code>cant-combined</code> elements have the two sets of accents superimposed,
in the (hard to read) style of the great manuscripts.)
</p>

<h2>The Decalogues: two versification policies</h2>

<p>A cv-number marks the <strong>start</strong> of a numbered verse. Across the Decalogues, the
three traditions differ only in <em>whose</em> chanted-verse starts they honor:</p>

<ul>
  <li><strong>MAM</strong> places a number at the start of every <strong>lower</strong> ({taxton}) verse.</li>
  <li><strong>BHS</strong> places a number at the start of every <strong>lower <em>or</em> upper</strong> verse — the
  union of the two cantillations' verse boundaries.</li>
  <li><strong>Sefaria</strong> is a hybrid: it honors the upper cantillation's extra boundary at
  the <em>early</em> split but not at the <em>late</em> split.</li>
</ul>

<p>Because BHS honors a superset of MAM's boundaries, every MAM Decalogue verse maps
to <em>one or more</em> whole BHS verses, never the reverse.</p>

<p>The whole story is then <em>how the two cantillations' boundaries sit relative to each
other</em> — and this differs between the two splits. At the <strong>early</strong> split they
<strong>overlap</strong> (the splits interleave); at the <strong>late</strong> split the upper is <strong>strictly
contained within</strong> a single lower verse.</p>

<h3>The early split — overlapping boundaries</h3>

<p>Here the {taxton} and {elyon} place their verse-ends at <em>different</em> points, and
neither's boundaries nest inside the other's. Inside what {taxton} reads as one
verse (MAM 20:2), the {elyon} ends a verse early, at {early_elyon_avadim}
(<em>silluq</em> / <em>sof pasuq</em>), where {taxton} has only <em>etnaḥta</em>
({early_taxton_avadim}) and reads on. Conversely, where {taxton} ends at
{early_taxton_panai} (<em>sof pasuq</em>), the {elyon} has only <em>revia</em>
({early_elyon_panai}) and reads on — its verse running to {early_mitsvotai}
(end of MAM 20:5). So the two sets of splits interleave rather than nest.</p>

<p>In the table below each end-word carries its own strand's mark: a bare <em>sof pasuq</em>
(<code>׃</code>) means that strand ends its verse there; an ordinary accent means it reads
on. Within each cantillation a chanted verse's <strong>first</strong> word is shown in green
(<em>start</em>) and its <strong>last</strong> word in red (<em>stop</em>); the words between (and the <code>…</code>)
are left plain. The one long {elyon} verse ({early_elyrow_long}) has no verse-end of
its own until מצותי, so across the four {taxton} rows it spans (MAM 20:2b–20:5) only
its opening word (green, in the 20:2b row) and closing word (red, in the 20:5 row)
are colored.</p>

<table>
  <tr>
    <th>{taxton}</th>
    <th>{elyon}</th>
    <th>MAM</th>
    <th>BHS</th>
  </tr>
  <tr>
    <td>{early_row_201}</td>
    <td>{early_row_201}</td>
    <td>20:1</td>
    <td>20:1</td>
  </tr>
  <tr>
    <td>{early_taxrow_202a}</td>
    <td>{early_elyrow_202a}</td>
    <td rowspan="2">20:2</td>
    <td>20:2</td>
  </tr>
  <tr>
    <td>{early_taxrow_202b}</td>
    <td>{early_elyrow_202b}</td>
    <td>20:3</td>
  </tr>
  <tr>
    <td>{early_taxrow_203}</td>
    <td>{early_elyrow_203}</td>
    <td>20:3</td>
    <td>20:4</td>
  </tr>
  <tr>
    <td>{early_taxrow_204}</td>
    <td>{early_elyrow_204}</td>
    <td>20:4</td>
    <td>20:5</td>
  </tr>
  <tr>
    <td>{early_taxrow_205}</td>
    <td>{early_elyrow_205}</td>
    <td>20:5</td>
    <td>20:6</td>
  </tr>
  <tr>
    <td>…</td>
    <td>…</td>
    <td>…</td>
    <td>…</td>
  </tr>
  <tr>
    <td>{early_row_2011}</td>
    <td>{early_row_2011}</td>
    <td>20:11</td>
    <td>20:12</td>
  </tr>
</table>

<table dir="rtl">
  <tr>
    <th>{taxton}</th>
    <td>{early_taxrow_202a}</td>
    <td>{early_taxrow_202b}</td>
    <td>{early_taxrow_203}</td>
    <td>{early_taxrow_204}</td>
    <td>{early_taxrow_205}</td>
  </tr>
  <tr>
    <th>{elyon}</th>
    <td>{early_elyrow_202a}</td>
    <td>{early_elyrow_202b}</td>
    <td>{early_elyrow_203}</td>
    <td>{early_elyrow_204}</td>
    <td>{early_elyrow_205}</td>
  </tr>
</table>

<p>The {elyon}'s <em>second</em> merge — the Sabbath commandment, MAM 20:7–20:10 — reads
the same way, in the same transposed form. The {taxton} divides it into four verses (each
cell green-start / red-stop); the {elyon} reads all four as one verse, so only its outer
endpoints are colored — green on 20:7's start, red on 20:10's end — and the two interior
cells are wholly plain:</p>

<table dir="rtl">
  <tr>
    <th>{taxton}</th>
    <td>{sab_taxrow_7}</td>
    <td>{sab_taxrow_8}</td>
    <td>{sab_taxrow_9}</td>
    <td>{sab_taxrow_10}</td>
  </tr>
  <tr>
    <th>{elyon}</th>
    <td>{sab_elyrow_7}</td>
    <td>{sab_elyrow_8}</td>
    <td>{sab_elyrow_9}</td>
    <td>{sab_elyrow_10}</td>
  </tr>
</table>

<p>Because BHS numbers at every {taxton} <strong>or</strong> {elyon} verse-start (their union),
the lone {elyon} boundary that {taxton} lacks — at {early_elyon_avadim} —
adds one BHS verse: MAM's single 20:2 becomes BHS 20:2 / 20:3, and the rest of the
chapter shifts up by one. Sefaria matches BHS here; Deuteronomy 5:6 behaves
identically.</p>

<h3>The late split — nested boundaries</h3>

<p>Here the two cantillations <strong>share</strong> the outer boundary and the upper merely
subdivides the interior. In MAM Exodus 20:12 the lower cantillation runs the four
short commandments as a <strong>single</strong> verse; the upper gives each its own verse — all
four strictly contained within the one lower verse, both ending together at שקר:</p>

<table>
  <tr>
    <th>scripture order →</th>
    <th>"You shall not murder"</th>
    <th>"… commit adultery"</th>
    <th>"… steal"</th>
    <th>"… bear false witness"</th>
  </tr>
  <tr>
    <th>lower (MAM)</th>
    <td colspan="4">one verse — ends {late_taxton_end}</td>
  </tr>
  <tr>
    <th>upper</th>
    <td>ends {late_elyon_0}</td>
    <td>ends {late_elyon_1}</td>
    <td>ends {late_elyon_2}</td>
    <td>ends {late_elyon_3}</td>
  </tr>
  <tr>
    <th>MAM #</th>
    <td colspan="4">20:12</td>
  </tr>
  <tr>
    <th>BHS #</th>
    <td>20:13</td>
    <td>20:14</td>
    <td>20:15</td>
    <td>20:16</td>
  </tr>
  <tr>
    <th>Sef #</th>
    <td colspan="4">20:13</td>
  </tr>
</table>

<p>BHS numbers at each upper start, giving <strong>four verses where MAM has one</strong>.
Sefaria, unlike BHS, does <strong>not</strong> honor the upper cantillation here — it keeps
MAM's single verse (one number). This late split is the one place where Sefaria and
BHS part ways. Deuteronomy 5:16 works identically.</p>

<h2>Numbers 25/26: a break at an <em>etnaḥta</em>, not a <em>sof pasuq</em></h2>

<p>This boundary is cantillational in the <strong>opposite</strong> way. Here there is only one
cantillation, and its verdict is <em>negative</em>: at the point BHS splits, cantillation
marks <strong>not</strong> a verse end but a mid-verse <em>etnaḥta</em>.</p>

<p>MAM keeps Numbers 26:1 as a <strong>single chanted verse</strong> whose interior carries a
mid-verse paragraph break — a פסקא באמצע פסוק (here a <em>petuḥah</em>). The break is shown
below as a line break, which is what a <em>petuḥah</em> ("open" section) in fact is: the text
after it resumes on a fresh line. Both lines are one and the same chanted verse:</p>

<blockquote class="verse">
{num_seg0}<br>
{num_seg1_first} … {num_seg1_last}
</blockquote>

<p>The verse ends, as always, at <em>sof pasuq</em> ({num_seg1_last}); the word before the
break, {num_seg0_last}, carries only <em>etnaḥta</em> — the strongest <strong>mid-verse</strong>
disjunctive, but not a verse end. BHS promotes that break to a verse <strong>and</strong> chapter
boundary, making its 25:19 end at {num_seg0_last} — on an <em>etnaḥta</em>, <strong>not</strong> a
<em>sof pasuq</em>. So BHS's 25:19 is not a chanted verse; the MAM-simple data marks it
<code>ends-with-sampe: "pe2"</code> and <code>contents-corresponds-to: "less than a full verse in
MAM"</code>. Sefaria, like MAM, keeps the single verse.</p>

<p>Why did BHS make this a <em>chapter</em> boundary as well? The <em>etnaḥta</em> and its
accompanying פסקא באמצע פסוק already signal a strong break here; perhaps someone
nonetheless felt that a chapter break was needed to communicate an even stronger break
at this point. Or perhaps this chapter break has its origin in a non-cantillated
(perhaps even non-Hebrew) version of the text, where its defiance of the chanted verse
boundary becomes irrelevant (or at least invisible).</p>

<p>Note what is and isn't doing the work. The פסקא באמצע פסוק is <strong>not</strong> the cause and
is not part of the cantillation — such mid-verse paragraph breaks occur in
<a href="{pbp_foi_url}">many verses</a> no tradition splits (e.g. Deuteronomy 2:8); here it merely <strong>reinforces</strong> a
division the <em>etnaḥta</em> already marks. And it is that <em>etnaḥta</em> that explains both
sides: why there is a strong division to split on, and why a cantillation-sensitive
versification like MAM's refuses to treat it as a verse end — a mid-verse pause, however
strong, is still mid-verse.</p>

<p>The contrast with the Decalogues is the point: there, BHS's extra boundaries <strong>are</strong>
real chanted-verse ends (in the other cantillation); here, BHS's extra boundary is
<strong>not</strong> a chanted-verse end in any cantillation — it lands on an <em>etnaḥta</em>.</p>

<h2>Summary</h2>

<table>
  <tr>
    <th>Passage</th>
    <th>MAM numbers at</th>
    <th>BHS numbers at</th>
    <th>Sefaria</th>
    <th>Boundary relationship</th>
  </tr>
  <tr>
    <td>Decalogues — early (Exod 20:2, Deut 5:6)</td>
    <td>lower starts</td>
    <td>lower <strong>or</strong> upper starts</td>
    <td>as BHS</td>
    <td>dual cantillation — <strong>overlapping</strong></td>
  </tr>
  <tr>
    <td>Decalogues — late (Exod 20:12, Deut 5:16)</td>
    <td>lower starts</td>
    <td>lower <strong>or</strong> upper starts</td>
    <td>lower starts only</td>
    <td>dual cantillation — <strong>nested</strong></td>
  </tr>
  <tr>
    <td>Numbers 25/26</td>
    <td>chanted-verse starts</td>
    <td>+ mid-verse break (onto <em>etnaḥta</em>)</td>
    <td>as MAM</td>
    <td>break at <em>etnaḥta</em>, not <em>sof pasuq</em></td>
  </tr>
</table>

<p>In the Decalogues, MAM's numbered boundaries coincide with lower chanted-verse
ends, and BHS's extra boundaries are upper chanted-verse ends. In Numbers 25/26 BHS's
extra boundary is not a chanted-verse end in <em>any</em> cantillation — it lands on an
<em>etnaḥta</em>. That is the whole cantillational story behind these versification
differences.</p>

<p>The other differences catalogued in
<a href="{vdiff_url}">versification-differences.md</a> — the 1 Samuel 23/24
and Jeremiah 30/31 chapter-boundary shifts, and the Joshua 21 present-vs-absent
case — are <strong>not</strong> cantillational: the first two shift only a chapter <em>number</em>
across a boundary both traditions already agree on, and the third is a genuine
difference of text.</p>
"""


def render_full_html(books_mpu):
    examples = strands.gather_examples(books_mpu)
    late = examples.pop("late_elyon_ends")
    fields = {
        "vdiff_url": _VDIFF_URL,
        "pbp_foi_url": _PBP_FOI_URL,
        "taxton": _TAXTON,
        "elyon": _ELYON,
        **examples,
        **{f"late_elyon_{i}": w for i, w in enumerate(late)},
    }
    comment = provenance.generated_html_comment(_GENERATOR_FILE)
    body = _BODY_TEMPLATE.format(**fields)
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
