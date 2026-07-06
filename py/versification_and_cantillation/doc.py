"""Render the generated versification-and-cantillation Markdown document.

Prose is authored here; the Hebrew example words are pulled byte-faithfully from
the upstream MAM-parsed-plus data via `strands.gather_examples` so the generated
output stays in lockstep with the source text.
"""

from pathlib import Path

from mb_cmn import provenance
from versification_and_cantillation import strands

_GENERATOR_FILE = Path(__file__).with_name("generate_doc.py")

# str.format template. The only braces in the body are the {placeholders} below;
# all Hebrew example words are substituted from data. Latin transliteration uses
# precomposed "h with dot below" (U+1E25 = NFC), per MAM-basics issue #187.
_TEMPLATE = """\
# Versification and Cantillation

This is a companion to
[versification-differences.md](versification-differences.md). That document
deliberately treats a "verse" as nothing more than the span of text between two
cv-labels, ignoring cantillation. This document discusses the
cases in which cantillation helps explain why the versification
differences arose: the four Decalogue splits and the Numbers 25/26 boundary.

Every MAM numbered verse ends at a *sof pasuq* — all 23,202 numbered verses, not
just the cases below. But some MAM numbered verses in the Decalogues have one
or more "extra" *sof pasuq* marks besides the one at the end.
It is at these places where the Decalogue versification differences occur,
because BHS ends a numbered verse at these "extra" *sof pasuq* marks, too.
(The Sefaria Decalogues have a mix of MAM and BHS versification.)

The difference regarding the Numbers 25/26 boundary
has little in common with the Decalogue cases.
There in Numbers, BHS splits the chanted verse that MAM calls 26:1 into
a 25:19 span (a verse number that does not exist in MAM)
and a 26:1 span.
BHS 26:1 starts right after an *etnaḥta*.
Although this *etnaḥta* is reinforced with a פסקא באמצע פסוק,
perhaps someone felt that a chapter break, too,
was needed to communicate an even stronger break at this point.
Or, perhaps this chapter break has its origin in a
non-cantillated (perhaps even non-Hebrew) version of the text.
In such a text, this chapter break's defiance of the chanted verse boundary
becomes irrelevant (or at least invisible).

## Terminology

- **Chanted verse** — a span that ends where the cantillation ends a verse: the
  strong disjunctive *silluq* on the last stressed syllable, immediately followed
  by *sof pasuq* (the `׃` mark). A *sof pasuq* is the visible signature of a
  chanted-verse end. (*Silluq* is only that verse-final mark; the identical-looking
  mark elsewhere in a verse is an ordinary *meteg*, a metrical mark, not a
  verse-end. Likewise the vertical stroke of *paseq* / *legarmeh* is unrelated —
  it is not a verse boundary.)
- **The two Decalogues.** The Decalogue carries **two** parallel cantillations.
  The **lower** (*taḥton*, תחתון) parses the passage into ordinary-length verses;
  the **upper** (*elyon*, עליון) favors a different division of the text, most
  strikingly with four very short (two-word) verses toward the end. MAM numbers
  the Decalogue by the **lower** cantillation. In the MAM-simple data these strands
  are the `cant-alef` (lower / *taḥton*) and `cant-bet` (upper / *elyon*) elements,
  with `cant-combined` the two superimposed.

## The Decalogue: two numbering policies

A cv-number marks the **start** of a numbered verse. Across the Decalogue the
three traditions differ only in *whose* chanted-verse starts they honor:

- **MAM** places a number at the start of every **lower** (*taḥton*) verse.
- **BHS** places a number at the start of every **lower *or* upper** verse — the
  union of the two cantillations' verse boundaries.
- **Sefaria** is a hybrid: it honors the upper cantillation's extra boundary at
  the *early* split but not at the *late* split.

Because BHS honors a superset of MAM's boundaries, every MAM Decalogue verse maps
to *one or more* whole BHS verses, never the reverse. (Outside the Decalogue there
is only one cantillation, so "lower or upper" collapses to it and all three
traditions agree.)

The whole story is then *how the two cantillations' boundaries sit relative to each
other* — and this differs between the two splits. At the **early** split they
**overlap** (the splits interleave); at the **late** split the upper is **strictly
contained within** a single lower verse.

### The early split — overlapping boundaries

Here the *taḥton* and *elyon* place their verse-ends at *different* points, and
neither's boundaries nest inside the other's. Inside what *taḥton* reads as one
verse (MAM 20:2), the *elyon* ends a verse early, at {early_elyon_avadim}
(*silluq* / *sof pasuq*), where *taḥton* has only *etnaḥta*
({early_taxton_avadim}) and reads on. Conversely, where *taḥton* ends at
{early_taxton_panai} (*sof pasuq*), the *elyon* has only *revia*
({early_elyon_panai}) and reads on — its verse running to {early_mitsvotai}
(end of MAM 20:5). So the two sets of splits interleave rather than nest.

In the table below each end-word carries its own strand's mark: a bare *sof pasuq*
(`׃`) means that strand ends its verse there; an ordinary accent means it reads
on. The one long *elyon* verse ({early_elyrow_long}) spans four *taḥton*
verses, shown as the merged cell.

<table>
  <tr>
    <th><em>taḥton</em></th>
    <th><em>elyon</em></th>
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
    <td>20:2a</td>
    <td>20:2</td>
  </tr>
  <tr>
    <td>{early_taxrow_202b}</td>
    <td rowspan="4">{early_elyrow_long}</td>
    <td>20:2b</td>
    <td>20:3</td>
  </tr>
  <tr>
    <td>{early_taxrow_203}</td>
    <td>20:3</td>
    <td>20:4</td>
  </tr>
  <tr>
    <td>{early_taxrow_204}</td>
    <td>20:4</td>
    <td>20:5</td>
  </tr>
  <tr>
    <td>{early_taxrow_205}</td>
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

Because BHS numbers at every *taḥton* **or** *elyon* verse-start (their union),
the lone *elyon* boundary that *taḥton* lacks — at {early_elyon_avadim} —
adds one BHS verse: MAM's single 20:2 becomes BHS 20:2 / 20:3, and the rest of the
chapter shifts up by one. Sefaria matches BHS here; Deuteronomy 5:6 behaves
identically.

### The late split — nested boundaries

Here the two cantillations **share** the outer boundary and the upper merely
subdivides the interior. In MAM Exodus 20:12 the lower cantillation runs the four
short commandments as a **single** verse; the upper gives each its own verse — all
four strictly contained within the one lower verse, both ending together at שקר:

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

BHS numbers at each upper start, giving **four verses where MAM has one**.
Sefaria, unlike BHS, does **not** honor the upper cantillation here — it keeps
MAM's single verse (one number). This late split is the one place where Sefaria and
BHS part ways. Deuteronomy 5:16 works identically.

## Numbers 25/26: a break at an *etnaḥta*, not a *sof pasuq*

This boundary is cantillational in the **opposite** way. Here there is only one
cantillation, and its verdict is *negative*: at the point BHS splits, cantillation
marks **not** a verse end but a mid-verse *etnaḥta*.

MAM keeps Numbers 26:1 as a **single chanted verse** whose interior carries a
mid-verse paragraph break — a פסקא באמצע פסוק (here a *petuḥah*):

> {num_seg0} &nbsp;[*petuḥah*]&nbsp; {num_seg1_first} … {num_seg1_last}

The verse ends, as always, at *sof pasuq* ({num_seg1_last}); the word before the
break, {num_seg0_last}, carries only *etnaḥta* — the strongest **mid-verse**
disjunctive, but not a verse end. BHS promotes that break to a verse **and** chapter
boundary, making its 25:19 end at {num_seg0_last} — on an *etnaḥta*, **not** a
*sof pasuq*. So BHS's 25:19 is not a chanted verse; the MAM-simple data marks it
`ends-with-sampe: "pe2"` and `contents-corresponds-to: "less than a full verse in
MAM"`. Sefaria, like MAM, keeps the single verse.

Note what is and isn't doing the work. The פסקא באמצע פסוק is **not** the cause and
is not part of the cantillation — such mid-verse paragraph breaks occur in many
verses no tradition splits (e.g. Genesis 35:22); here it merely **reinforces** a
division the *etnaḥta* already marks. And it is that *etnaḥta* that explains both
sides: why there is a strong division to split on, and why a cantillation-sensitive
numbering like MAM's refuses to treat it as a verse end — a mid-verse pause, however
strong, is still mid-verse.

The contrast with the Decalogue is the point: there, BHS's extra boundaries **are**
real chanted-verse ends (in the other cantillation); here, BHS's extra boundary is
**not** a chanted-verse end in any cantillation — it lands on an *etnaḥta*.

## Summary

| Passage | MAM numbers at | BHS numbers at | Sefaria | Boundary relationship |
|---|---|---|---|---|
| Decalogue — early (Exod 20:2, Deut 5:6) | lower starts | lower **or** upper starts | as BHS | dual cantillation — **overlapping** |
| Decalogue — late (Exod 20:12, Deut 5:16) | lower starts | lower **or** upper starts | lower starts only | dual cantillation — **nested** |
| Numbers 25/26 | chanted-verse starts | + mid-verse break (onto *etnaḥta*) | as MAM | break at *etnaḥta*, not *sof pasuq* |

In every Decalogue case MAM's numbered boundaries coincide with lower chanted-verse
ends, and BHS's extra boundaries are upper chanted-verse ends. In Numbers 25/26 BHS's
extra boundary is not a chanted-verse end in *any* cantillation — it lands on an
*etnaḥta*. That is the whole cantillational story behind these versification
differences.

The other differences catalogued in
[versification-differences.md](versification-differences.md) — the 1 Samuel 23/24
and Jeremiah 30/31 chapter-boundary shifts, and the Joshua 21 present-vs-absent
case — are **not** cantillational: the first two shift only a chapter *number*
across a boundary both traditions already agree on, and the third is a genuine
difference of text.
"""


def render_full_markdown(books_mpu):
    examples = strands.gather_examples(books_mpu)
    late = examples.pop("late_elyon_ends")
    fields = {**examples, **{f"late_elyon_{i}": w for i, w in enumerate(late)}}
    header = f"<!-- {provenance.generated_html_comment(_GENERATOR_FILE)} -->\n"
    return header + "\n" + _TEMPLATE.format(**fields)
